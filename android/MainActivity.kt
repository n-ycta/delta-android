package dev.delta.android
import android.os.Bundle
import android.content.Intent
import dev.delta.android.platform.*
class MainActivity:TauriActivity(){
 override fun onCreate(state:Bundle?){NativeCore.ensure(this);PlatformControls.attach(this);super.onCreate(state);PlatformControls.resume(this)}
 override fun onNewIntent(intent:Intent){super.onNewIntent(intent);setIntent(intent);PlatformControls.accept(intent)}
 @Deprecated("Legacy result API required for the shared document picker")
 override fun onActivityResult(request:Int,result:Int,data:Intent?){if(!PlatformControls.onResult(this,request,result,data))super.onActivityResult(request,result,data)}
}
