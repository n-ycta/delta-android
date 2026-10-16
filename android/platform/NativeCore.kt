package dev.delta.android.platform
import android.content.Context
import java.io.File
class NativeCore { companion object {
 init{System.loadLibrary("delta_android_lib")}
 @JvmStatic external fun start(context:Context,path:String):Boolean
 @JvmStatic external fun stop()
 @JvmStatic external fun info():String
 @JvmStatic external fun poll():String
 @JvmStatic external fun acknowledge(keys:String)
 @JvmStatic fun ensure(context:Context){check(start(context.applicationContext,File(context.filesDir,"node").canonicalPath)){"Cannot open the private node profile. Data was not reset."}}
}}
