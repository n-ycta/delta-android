#[cfg_attr(mobile,tauri::mobile_entry_point)]
pub fn run(){delta_native_host::run(tauri::generate_context!());}
