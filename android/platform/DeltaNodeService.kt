package dev.delta.android.platform
import android.app.*
import android.content.*
import android.os.IBinder
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit
import org.json.JSONArray
class DeltaNodeService:Service(){companion object{@Volatile var running=false}
 private val worker=Executors.newSingleThreadScheduledExecutor()
 override fun onBind(intent:Intent?):IBinder?=null
 override fun onCreate(){super.onCreate();PlatformControls.channel(this);val open=PendingIntent.getActivity(this,0,packageManager.getLaunchIntentForPackage(packageName),PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT);val stop=PendingIntent.getService(this,1,Intent(this,DeltaNodeService::class.java).setAction("stop"),PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT);startForeground(7700,Notification.Builder(this,"delta.node").setSmallIcon(android.R.drawable.ic_dialog_info).setContentTitle("Delta").setContentText("Node is running · Узел работает").setContentIntent(open).setOngoing(true).addAction(Notification.Action.Builder(null,"Stop / Стоп",stop).build()).build());running=true
  worker.scheduleWithFixedDelay({try{NativeCore.ensure(this);if(PlatformControls.notifications(this)){val rows=JSONArray(NativeCore.poll());for(i in 0 until rows.length()){val row=rows.getJSONObject(i);val intent=packageManager.getLaunchIntentForPackage(packageName)!!.putExtra("route",row.optString("route"));val pending=PendingIntent.getActivity(this,row.getString("id").hashCode(),intent,PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE);val body=row.optString("body").take(2000);(getSystemService(NOTIFICATION_SERVICE)as NotificationManager).notify(row.getString("id").hashCode(),Notification.Builder(this,"delta.alerts").setSmallIcon(android.R.drawable.ic_dialog_info).setContentTitle(row.getString("title").take(200)).setContentText(body).setStyle(Notification.BigTextStyle().bigText(body)).setContentIntent(pending).setAutoCancel(true).build());NativeCore.acknowledge(JSONArray().put(row.getString("id")).toString())}}}catch(_:Exception){/* Persistent data remains intact; next poll retries. */}},0,30,TimeUnit.SECONDS)
 }
 override fun onStartCommand(intent:Intent?,flags:Int,startId:Int):Int{if(intent?.action=="stop"){getSharedPreferences("delta.lifecycle",MODE_PRIVATE).edit().putBoolean("background",false).apply();worker.execute{NativeCore.stop();stopSelf()};return START_NOT_STICKY};return START_STICKY}
 override fun onDestroy(){running=false;worker.shutdownNow();super.onDestroy()}
}
class BootReceiver:BroadcastReceiver(){override fun onReceive(context:Context,intent:Intent){if((intent.action==Intent.ACTION_BOOT_COMPLETED||intent.action==Intent.ACTION_MY_PACKAGE_REPLACED)&&context.getSharedPreferences("delta.lifecycle",Context.MODE_PRIVATE).getBoolean("background",false)){try{PlatformControls.start(context)}catch(_:Exception){/* OS restrictions require launching the app; never bypass policy. */}}}}
