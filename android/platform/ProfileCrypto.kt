package dev.delta.android.platform
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.KeyProperties
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec
/** Non-exportable Android Keystore AES key. No plaintext fallback or recoverable key in preferences. */
class ProfileCrypto { companion object {
 private const val alias="dev.delta.profile.v1"
 @Synchronized private fun key():SecretKey {val store=KeyStore.getInstance("AndroidKeyStore").apply{load(null)};if(!store.containsAlias(alias)){val generator=KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES,"AndroidKeyStore");generator.init(KeyGenParameterSpec.Builder(alias,KeyProperties.PURPOSE_ENCRYPT or KeyProperties.PURPOSE_DECRYPT).setBlockModes(KeyProperties.BLOCK_MODE_GCM).setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE).setRandomizedEncryptionRequired(true).build());generator.generateKey()};return store.getKey(alias,null) as SecretKey}
 @JvmStatic fun transform(operation:String,input:ByteArray):ByteArray {require(input.size<=4_000_000);val cipher=Cipher.getInstance("AES/GCM/NoPadding");val aad="dev.delta.profile.v1".toByteArray();return when(operation){"seal"->{cipher.init(Cipher.ENCRYPT_MODE,key());cipher.updateAAD(aad);byteArrayOf(68,76,67,49)+cipher.iv+cipher.doFinal(input)};"open"->{require(input.size>=32&&input.copyOfRange(0,4).contentEquals(byteArrayOf(68,76,67,49))){"Invalid encrypted profile"};cipher.init(Cipher.DECRYPT_MODE,key(),GCMParameterSpec(128,input.copyOfRange(4,16)));cipher.updateAAD(aad);cipher.doFinal(input.copyOfRange(16,input.size))};else->error("Unsupported crypto operation")}}
}}
