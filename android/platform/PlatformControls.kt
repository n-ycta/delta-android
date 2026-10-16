package dev.delta.android.platform
import android.Manifest
import android.app.*
import android.content.*
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import java.lang.ref.WeakReference
import java.util.concurrent.CompletableFuture
import java.util.concurrent.TimeUnit
import org.json.JSONObject
class PlatformControls {companion object {
 @Volatile private var activity=WeakReference<Activity>(null)
 @Volatile private var pending:CompletableFuture<Boolean>?=null
 @Volatile private var exportText=""
 @Volatile private var pairing:String?=null
 @Volatile private var route:String?=null
 private const val requestExport=8271
 fun attach(a:Activity){activity=WeakReference(a);accept(a.intent)}
 fun accept(intent:Intent?){intent?.data?.let{if(it.scheme=="delta"&&it.host=="pair"&&it.toString().length<=2048){pairing=it.toString();android.util.Log.i("DeltaLifecycle","Pairing invitation queued")}};intent?.getStringExtra("route")?.let{if(it.startsWith("/plugins/"))route=it.take(512)}}
 fun resume(context:Context){if(prefs(context).getBoolean("background",false))start(context)}
 private fun prefs(c:Context)=c.getSharedPreferences("delta.lifecycle",Context.MODE_PRIVATE)
 fun permitted(c:Context)=Build.VERSION.SDK_INT<33||c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS)==PackageManager.PERMISSION_GRANTED
 fun channel(c:Context){(c.getSystemService(Context.NOTIFICATION_SERVICE)as NotificationManager).createNotificationChannel(NotificationChannel("delta.node","Delta node",NotificationManager.IMPORTANCE_LOW));(c.getSystemService(Context.NOTIFICATION_SERVICE)as NotificationManager).createNotificationChannel(NotificationChannel("delta.alerts","Delta notifications",NotificationManager.IMPORTANCE_DEFAULT))}
 fun start(c:Context){c.startForegroundService(Intent(c,DeltaNodeService::class.java))}
 private fun requestPermission(){val a=activity.get()?:return;if(Build.VERSION.SDK_INT>=33&&!permitted(a))a.runOnUiThread{a.requestPermissions(arrayOf(Manifest.permission.POST_NOTIFICATIONS),8272)}}
 fun onResult(a:Activity,request:Int,result:Int,data:Intent?):Boolean{if(request!=requestExport)return false;try{val uri=data?.data;if(result==Activity.RESULT_OK&&uri!=null){a.contentResolver.openOutputStream(uri,"wt").use{out->checkNotNull(out).write(exportText.toByteArray())};pending?.complete(true)}else pending?.complete(false)}catch(e:Exception){pending?.completeExceptionally(IllegalStateException("Export failed"))}finally{exportText=""};return true}
 @JvmStatic fun dispatch(context:Context,method:String,input:String):String {val a=JSONObject(input);val answer=JSONObject();when(method){
 "status","info"->{answer.put("kind","android").put("backgroundRunning",DeltaNodeService.running).put("backgroundEnabled",prefs(context).getBoolean("background",false)).put("notifications",prefs(context).getBoolean("notifications",false)).put("notificationPermission",permitted(context));synchronized(this){answer.put("pendingPairing",pairing).put("pendingRoute",route);if(method=="status"){if(pairing!=null)android.util.Log.i("DeltaLifecycle","Pairing invitation delivered");pairing=null;route=null}}}
 "background"->{val enabled=a.optBoolean("enabled");prefs(context).edit().putBoolean("background",enabled).apply();if(enabled){requestPermission();NativeCore.ensure(context);start(context)}else context.stopService(Intent(context,DeltaNodeService::class.java));answer.put("enabled",enabled)}
 "notify"->{if(a.has("enabled")){val enabled=a.optBoolean("enabled");prefs(context).edit().putBoolean("notifications",enabled).apply();if(enabled)requestPermission();answer.put("enabled",enabled)}else{check(permitted(context)){"Notification permission required"};channel(context);val title=a.optString("title","Delta").take(200);val body=a.optString("body").take(2000);(context.getSystemService(Context.NOTIFICATION_SERVICE)as NotificationManager).notify((System.currentTimeMillis()%Int.MAX_VALUE).toInt(),Notification.Builder(context,"delta.alerts").setSmallIcon(android.R.drawable.ic_dialog_info).setContentTitle(title).setContentText(body).setStyle(Notification.BigTextStyle().bigText(body)).setAutoCancel(true).build());answer.put("sent",true)}}
 "open"->{val uri=Uri.parse(a.getString("url"));require(uri.scheme in listOf("http","https")&&uri.userInfo==null);val ui=activity.get()?:error("Activity unavailable");ui.runOnUiThread{ui.startActivity(Intent(Intent.ACTION_VIEW,uri))};answer.put("opened",true)}
 "share"->{val text=a.get("data").toString();require(text.length<=65536);val ui=activity.get()?:error("Activity unavailable");ui.runOnUiThread{ui.startActivity(Intent.createChooser(Intent(Intent.ACTION_SEND).setType("text/plain").putExtra(Intent.EXTRA_TEXT,text),"Delta"))};answer.put("shared",true)}
 "export"->{val markdown=a.optString("format")=="markdown";val text=if(markdown)a.getString("text")else a.get("data").toString();require(text.toByteArray().size<=32768);val ui=activity.get()?:error("Activity unavailable");synchronized(this){check(pending==null){"Export already open"};pending=CompletableFuture();exportText=text};try{ui.runOnUiThread{ui.startActivityForResult(Intent(Intent.ACTION_CREATE_DOCUMENT).addCategory(Intent.CATEGORY_OPENABLE).setType(if(markdown)"text/markdown" else "application/json").putExtra(Intent.EXTRA_TITLE,if(markdown)"delta-recovery.md" else "delta-export.json"),requestExport)};answer.put("saved",pending!!.get(120,TimeUnit.SECONDS))}finally{synchronized(this){pending=null;exportText=""}}}
 else->error("Unsupported platform operation")};return answer.toString()}
 fun notifications(c:Context)=prefs(c).getBoolean("notifications",false)&&permitted(c)
}}
