package dev.delta.android.platform
import android.app.Activity
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import android.net.ConnectivityManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import java.io.File
import java.security.MessageDigest
import org.json.JSONArray
import org.json.JSONObject
/** In-app update support. Download and checksum verification happen in the Rust host; this only reports the environment
 *  and starts the system installer, which always shows its own confirmation and enforces that the signature matches.
 *  Whether an update is available is decided by the semver comparison in Rust; here we only refuse an explicit
 *  versionCode downgrade (equal codes are allowed: rc and final builds share one). Android itself rejects real
 *  downgrades and signature mismatches. The file is re-hashed while it is copied into the install session. */
object AppUpdate {
 const val ACTION="dev.delta.android.UPDATE_STATUS"
 fun env(c:Context):JSONObject{
  val info=c.packageManager.getPackageInfo(c.packageName,0)
  val cm=c.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
  return JSONObject().put("versionName",info.versionName?:"0.0.0").put("versionCode",info.longVersionCode).put("metered",cm.isActiveNetworkMetered).put("abis",JSONArray(Build.SUPPORTED_ABIS.toList())).put("cacheDir",c.cacheDir.absolutePath).put("canInstall",c.packageManager.canRequestPackageInstalls())
 }
 /** Never throws: the JNI bridge would reduce any exception to a generic failure, so errors are returned as codes. */
 fun install(c:Context,activity:Activity?,path:String,sha256:String?):JSONObject{
  val installer=c.packageManager.packageInstaller
  var id=-1
  try{
   val expected=sha256?.lowercase()
   if(expected==null||!Regex("[0-9a-f]{64}").matches(expected))return fail("update_invalid")
   val dir=File(c.cacheDir,"updates").canonicalFile;val apk=File(path).canonicalFile
   if(apk.parentFile!=dir||apk.name!="delta.apk"||!apk.isFile)return fail("update_not_ready")
   val archive=c.packageManager.getPackageArchiveInfo(apk.path,0)?:return fail("update_invalid")
   val current=c.packageManager.getPackageInfo(c.packageName,0)
   if(archive.packageName!=c.packageName)return fail("update_invalid")
   if(archive.longVersionCode<current.longVersionCode)return fail("not_newer")
   if(!c.packageManager.canRequestPackageInstalls()){
    activity?.runOnUiThread{activity.startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:"+c.packageName)))}
    return fail("install_permission_required")
   }
   for(old in installer.mySessions)try{installer.abandonSession(old.sessionId)}catch(_:Exception){}
   val params=PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);params.setAppPackageName(c.packageName)
   id=installer.createSession(params)
   val digest=MessageDigest.getInstance("SHA-256")
   installer.openSession(id).use{s->
    apk.inputStream().use{input->s.openWrite("delta.apk",0,apk.length()).use{out->
     val buf=ByteArray(65536)
     while(true){val n=input.read(buf);if(n<0)break;digest.update(buf,0,n);out.write(buf,0,n)}
     s.fsync(out)
    }}
    if(digest.digest().joinToString(""){"%02x".format(it)}!=expected){
     android.util.Log.w("DeltaUpdate","Checksum mismatch")
     try{installer.abandonSession(id)}catch(_:Exception){}
     id=-1
     return fail("checksum_mismatch")
    }
    val callback=Intent(c,UpdateStatusReceiver::class.java).setAction(ACTION)
    // The installer fills in status extras, so the PendingIntent must be mutable on Android 12+.
    val flags=PendingIntent.FLAG_UPDATE_CURRENT or if(Build.VERSION.SDK_INT>=31)PendingIntent.FLAG_MUTABLE else 0
    s.commit(PendingIntent.getBroadcast(c,id,callback,flags).intentSender)
   }
   return JSONObject().put("prompted",true)
  }catch(e:Exception){
   android.util.Log.w("DeltaUpdate","Install failed",e)
   if(id>=0)try{installer.abandonSession(id)}catch(_:Exception){}
   return fail("install_failed")
  }
 }
 private fun fail(code:String)=JSONObject().put("error",code)
}
/** Not exported, so only the system installer (through our PendingIntent) can reach it. Shows the confirmation dialog. */
class UpdateStatusReceiver:BroadcastReceiver(){
 override fun onReceive(context:Context,intent:Intent){
  if(intent.action!=AppUpdate.ACTION)return
  val status=intent.getIntExtra(PackageInstaller.EXTRA_STATUS,-1)
  val id=intent.getIntExtra(PackageInstaller.EXTRA_SESSION_ID,-1)
  val pm=context.packageManager
  if(pm.packageInstaller.mySessions.none{it.sessionId==id}){android.util.Log.w("DeltaUpdate","Ignored installer callback for an unknown session");return}
  if(status!=PackageInstaller.STATUS_PENDING_USER_ACTION){android.util.Log.i("DeltaUpdate","Installer status $status "+intent.getStringExtra(PackageInstaller.EXTRA_STATUS_MESSAGE));return}
  @Suppress("DEPRECATION") val confirm=if(Build.VERSION.SDK_INT>=33)intent.getParcelableExtra(Intent.EXTRA_INTENT,Intent::class.java)else intent.getParcelableExtra<Intent>(Intent.EXTRA_INTENT)
  val grants=Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION or Intent.FLAG_GRANT_PREFIX_URI_PERMISSION
  if(confirm==null||confirm.action!="android.content.pm.action.CONFIRM_INSTALL"||(confirm.flags and grants)!=0||confirm.data!=null||confirm.clipData!=null){android.util.Log.w("DeltaUpdate","Rejected installer confirmation intent");return}
  val target=confirm.resolveActivity(pm)
  if(target==null||target.packageName==context.packageName){android.util.Log.w("DeltaUpdate","Rejected installer confirmation target");return}
  context.startActivity(confirm.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
 }
}
