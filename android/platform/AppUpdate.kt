package dev.delta.android.platform
import android.app.Activity
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.content.pm.PackageInstaller
import android.net.ConnectivityManager
import android.net.Uri
import android.os.Build
import android.provider.Settings
import java.io.File
import org.json.JSONArray
import org.json.JSONObject
/** In-app update support. Download and checksum verification happen in the Rust host; this only reports the environment
 *  and starts the system installer, which always shows its own confirmation and enforces that the signature matches. */
object AppUpdate {
 const val ACTION="dev.delta.android.UPDATE_STATUS"
 @Volatile private var session=-1
 fun env(c:Context):JSONObject{
  val info=c.packageManager.getPackageInfo(c.packageName,0)
  val cm=c.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
  return JSONObject().put("versionName",info.versionName?:"0.0.0").put("versionCode",info.longVersionCode).put("metered",cm.isActiveNetworkMetered).put("abis",JSONArray(Build.SUPPORTED_ABIS.toList())).put("cacheDir",c.cacheDir.absolutePath).put("canInstall",c.packageManager.canRequestPackageInstalls())
 }
 /** Never throws: the JNI bridge would reduce any exception to a generic failure, so errors are returned as codes. */
 fun install(c:Context,activity:Activity?,path:String):JSONObject{
  try{
   val dir=File(c.cacheDir,"updates").canonicalFile;val apk=File(path).canonicalFile
   if(apk.parentFile!=dir||apk.name!="delta.apk"||!apk.isFile)return fail("update_not_ready")
   val archive=c.packageManager.getPackageArchiveInfo(apk.path,0)?:return fail("update_invalid")
   val current=c.packageManager.getPackageInfo(c.packageName,0)
   // Android itself also refuses downgrades and signature mismatches; this just fails early with a clear code.
   if(archive.packageName!=c.packageName||archive.longVersionCode<=current.longVersionCode)return fail("not_newer")
   if(!c.packageManager.canRequestPackageInstalls()){
    activity?.runOnUiThread{activity.startActivity(Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:"+c.packageName)))}
    return fail("install_permission_required")
   }
   val installer=c.packageManager.packageInstaller
   val params=PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);params.setAppPackageName(c.packageName)
   val id=installer.createSession(params)
   installer.openSession(id).use{s->
    apk.inputStream().use{input->s.openWrite("delta.apk",0,apk.length()).use{out->input.copyTo(out);s.fsync(out)}}
    val callback=Intent(c,Class.forName("dev.delta.android.MainActivity")).setAction(ACTION).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
    // The installer fills in status extras, so the PendingIntent must be mutable on Android 12+.
    val flags=PendingIntent.FLAG_UPDATE_CURRENT or if(Build.VERSION.SDK_INT>=31)PendingIntent.FLAG_MUTABLE else 0
    session=id
    s.commit(PendingIntent.getActivity(c,id,callback,flags).intentSender)
   }
   return JSONObject().put("prompted",true)
  }catch(e:Exception){android.util.Log.w("DeltaUpdate","Install failed",e);return fail("install_failed")}
 }
 /** Shows the system confirmation dialog. Only for the session this app created, and only the installer's own action. */
 fun onStatus(a:Activity,intent:Intent){
  if(intent.action!=ACTION)return
  val status=intent.getIntExtra(PackageInstaller.EXTRA_STATUS,-1)
  if(intent.getIntExtra(PackageInstaller.EXTRA_SESSION_ID,-2)!=session){android.util.Log.w("DeltaUpdate","Ignored installer callback for an unknown session");return}
  if(status==PackageInstaller.STATUS_PENDING_USER_ACTION){
   @Suppress("DEPRECATION") val confirm=if(Build.VERSION.SDK_INT>=33)intent.getParcelableExtra(Intent.EXTRA_INTENT,Intent::class.java)else intent.getParcelableExtra<Intent>(Intent.EXTRA_INTENT)
   if(confirm?.action=="android.content.pm.action.CONFIRM_INSTALL")a.startActivity(confirm)
  }else android.util.Log.i("DeltaUpdate","Installer status $status "+intent.getStringExtra(PackageInstaller.EXTRA_STATUS_MESSAGE))
 }
 private fun fail(code:String)=JSONObject().put("error",code)
}
