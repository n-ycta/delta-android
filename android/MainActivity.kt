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
 override fun onCreate(state:Bundle?){NativeCore.ensure(this);PlatformControls.attach(this);super.onCreate(state);val content=findViewById<View>(android.R.id.content);content.setBackgroundColor(Color.BLACK);content.setOnApplyWindowInsetsListener{view,insets->
 if(Build.VERSION.SDK_INT>=30){val bars=insets.getInsets(WindowInsets.Type.systemBars() or WindowInsets.Type.displayCutout());view.setPadding(bars.left,bars.top,bars.right,bars.bottom)}else{@Suppress("DEPRECATION") view.setPadding(insets.systemWindowInsetLeft,insets.systemWindowInsetTop,insets.systemWindowInsetRight,insets.systemWindowInsetBottom)};insets};content.requestApplyInsets();PlatformControls.resume(this)}
 override fun onWebViewCreate(webView:WebView){super.onWebViewCreate(webView);webView.importantForAccessibility=View.IMPORTANT_FOR_ACCESSIBILITY_YES}
 override fun onResume(){NativeCore.ensure(this);super.onResume();PlatformControls.attach(this);PlatformControls.resume(this)}
 override fun onNewIntent(intent:Intent){super.onNewIntent(intent);setIntent(intent);PlatformControls.accept(intent)}
 @Deprecated("Legacy result API required for the shared document picker")
 override fun onActivityResult(request:Int,result:Int,data:Intent?){if(!PlatformControls.onResult(this,request,result,data))super.onActivityResult(request,result,data)}
}
