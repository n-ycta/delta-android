#[cfg_attr(mobile,tauri::mobile_entry_point)]
pub fn run(){delta_native_host::run(tauri::generate_context!());}
#[cfg(target_os="android")]
mod service {
 use jni::{JNIEnv,objects::{JObject,JString,JClass},sys::{jboolean,jstring}};
 #[no_mangle]pub extern "system" fn Java_dev_delta_android_platform_NativeCore_start(mut env:JNIEnv,_class:JClass,context:JObject,path:JString)->jboolean {let path=match env.get_string(&path){Ok(v)=>std::path::PathBuf::from(v.to_string_lossy().into_owned()),Err(_)=>return 0};match delta_native_host::android::start(&mut env,context,path){Ok(())=>1,Err(_)=>{let _=env.exception_clear();0}}}
 #[no_mangle]pub extern "system" fn Java_dev_delta_android_platform_NativeCore_stop(_env:JNIEnv,_class:JClass){delta_native_host::android::stop()}
 #[no_mangle]pub extern "system" fn Java_dev_delta_android_platform_NativeCore_info(env:JNIEnv,_class:JClass)->jstring {let value=delta_native_host::android::active().map(|n|n.info("0.1.1","0.1.3")).unwrap_or_default().to_string();env.new_string(value).map(|s|s.into_raw()).unwrap_or(std::ptr::null_mut())}
 #[no_mangle]pub extern "system" fn Java_dev_delta_android_platform_NativeCore_poll(env:JNIEnv,_class:JClass)->jstring {env.new_string(delta_native_host::android::poll().to_string()).map(|s|s.into_raw()).unwrap_or(std::ptr::null_mut())}
 #[no_mangle]pub extern "system" fn Java_dev_delta_android_platform_NativeCore_acknowledge(mut env:JNIEnv,_class:JClass,keys:JString){if let Ok(v)=env.get_string(&keys){delta_native_host::android::acknowledge(&v.to_string_lossy())}}
}
