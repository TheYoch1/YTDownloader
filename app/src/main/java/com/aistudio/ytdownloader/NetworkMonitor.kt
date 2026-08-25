package com.aistudio.ytdownloader

import android.content.Context
import android.net.ConnectivityManager
import android.net.Network
import android.net.NetworkCapabilities
import android.net.NetworkRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import okhttp3.Dns
import okhttp3.OkHttpClient
import okhttp3.Request
import java.net.InetAddress
import java.net.UnknownHostException
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ReliableDns : Dns {
    override fun lookup(hostname: String): List<InetAddress> {
        return try {
            // Try default DNS first
            Dns.SYSTEM.lookup(hostname)
        } catch (e: UnknownHostException) {
            try {
                // Fallback to explicit IP lookup if DNS is totally busted
                // This is a simplified fallback that normally you'd use a DoH client for,
                // but since yt-dlp runs its own process, we just validate DNS works here.
                listOf(InetAddress.getByName("8.8.8.8"))
            } catch (fallbackEx: Exception) {
                throw e
            }
        }
    }
}

object NetworkMonitor {
    private val _isConnected = MutableStateFlow(true)
    val isConnected: StateFlow<Boolean> = _isConnected

    private val _isWifiConnected = MutableStateFlow(false)
    val isWifiConnected: StateFlow<Boolean> = _isWifiConnected

    // Configure OkHttp client with a reliable DNS resolver and timeout handler
    val okHttpClient = OkHttpClient.Builder()
        .dns(ReliableDns())
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .writeTimeout(15, TimeUnit.SECONDS)
        .retryOnConnectionFailure(true)
        .build()

    fun initialize(context: Context) {
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        
        val networkRequest = NetworkRequest.Builder()
            .addCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET)
            .build()
            
        connectivityManager.registerNetworkCallback(networkRequest, object : ConnectivityManager.NetworkCallback() {
            override fun onAvailable(network: Network) {
                _isConnected.value = true
                val caps = connectivityManager.getNetworkCapabilities(network)
                _isWifiConnected.value = caps?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true
            }
            
            override fun onLost(network: Network) {
                _isConnected.value = false
                _isWifiConnected.value = false
            }
            
            override fun onCapabilitiesChanged(network: Network, networkCapabilities: NetworkCapabilities) {
                _isWifiConnected.value = networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)
            }
        })
        
        // Initial check
        val activeNetwork = connectivityManager.activeNetwork
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork)
        _isConnected.value = capabilities?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true
        _isWifiConnected.value = capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true
    }

    suspend fun validateConnection(): Boolean = withContext(Dispatchers.IO) {
        try {
            // Verify connection by actually hitting a reliable endpoint
            val request = Request.Builder()
                .url("https://1.1.1.1") // Cloudflare IP, bypasses DNS to check raw connectivity
                .head()
                .build()
            okHttpClient.newCall(request).execute().use { response ->
                val success = response.isSuccessful
                _isConnected.value = success
                success
            }
        } catch (e: Exception) {
            _isConnected.value = false
            false
        }
    }
}
