package dev.delta.android
import android.os.Bundle
import android.content.Intent
import android.view.View
import android.webkit.WebView
import android.graphics.Color
import android.view.WindowInsets
import android.os.Build
import dev.delta.android.platform.*
class MainActivity:TauriActivity(){
 private var deltaWebView:WebView?=null
 override fun onCreate(state:Bundle?){
 // Stage reviewed static app packages for checksum verification; installation remains explicit.
 val bundled=java.io.File(dataDir,"bundled-apps");bundled.mkdirs()
 for(name in assets.list("delta-apps")?:emptyArray()){
  if(!name.matches(Regex("[a-z0-9.-]+\\.delta-app")))continue
  val target=java.io.File(bundled,name)
  assets.open("delta-apps/$name").use{input->target.outputStream().use{output->input.copyTo(output)}}
 }
 NativeCore.ensure(this);PlatformControls.attach(this);super.onCreate(state);val content=findViewById<View>(android.R.id.content);content.setBackgroundColor(Color.BLACK);content.setOnApplyWindowInsetsListener{view,insets->
 if(Build.VERSION.SDK_INT>=30){val bars=insets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout());view.setPadding(bars.left,bars.top,bars.right,bars.bottom)}else{@Suppress("DEPRECATION") view.setPadding(insets.systemWindowInsetLeft,insets.systemWindowInsetTop,insets.systemWindowInsetRight,insets.systemWindowInsetBottom)};insets};content.requestApplyInsets();PlatformControls.resume(this)}
 override fun onWebViewCreate(webView:WebView){super.onWebViewCreate(webView);deltaWebView=webView;webView.importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_YES}
 override fun onResume(){NativeCore.ensure(this);super.onResume();PlatformControls.attach(this);PlatformControls.resume(this);deliverPair(intent)}
 override fun onNewIntent(intent:Intent){setIntent(intent);PlatformControls.accept(intent);super.onNewIntent(intent);deliverPair(intent)}
 // One-shot: JS returns false until the page exposes __deltaAcceptPair; any result other than false consumes it.
 private fun deliverPair(intent:Intent?){val uri=intent?.data?:return;if(uri.scheme!="delta"||uri.host!="pair")return;val url=uri.toString();val quoted=org.json.JSONObject.quote(url);deltaWebView?.post{deltaWebView?.evaluateJavascript("(window.__deltaAcceptPair?(window.__deltaAcceptPair("+quoted+"),window.location.hash='#/settings?tab=connection',true):false)"){result->if(result!="false"){intent.setData(null);PlatformControls.consumePairing(url)}}}}
 @Deprecated("Legacy result API required for the shared document picker")
 override fun onActivityResult(request:Int,result:Int,data:Intent?){if(!PlatformControls.onResult(this,request,result,data))super.onActivityResult(request,result,data)}
}
