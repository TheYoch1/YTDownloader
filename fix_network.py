import re

with open("app/src/main/java/com/aistudio/ytdownloader/NetworkMonitor.kt", "r") as f:
    content = f.read()

target = '''    private val _isConnected = MutableStateFlow(true)
    val isConnected: StateFlow<Boolean> = _isConnected'''

rep = '''    private val _isConnected = MutableStateFlow(true)
    val isConnected: StateFlow<Boolean> = _isConnected

    private val _isWifiConnected = MutableStateFlow(false)
    val isWifiConnected: StateFlow<Boolean> = _isWifiConnected'''

content = content.replace(target, rep)

target2 = '''            override fun onAvailable(network: Network) {
                _isConnected.value = true
            }
            
            override fun onLost(network: Network) {
                _isConnected.value = false
            }'''

rep2 = '''            override fun onAvailable(network: Network) {
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
            }'''

content = content.replace(target2, rep2)

target3 = '''        // Initial check
        val activeNetwork = connectivityManager.activeNetwork
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork)
        _isConnected.value = capabilities?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true'''

rep3 = '''        // Initial check
        val activeNetwork = connectivityManager.activeNetwork
        val capabilities = connectivityManager.getNetworkCapabilities(activeNetwork)
        _isConnected.value = capabilities?.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET) == true
        _isWifiConnected.value = capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true'''

content = content.replace(target3, rep3)

with open("app/src/main/java/com/aistudio/ytdownloader/NetworkMonitor.kt", "w") as f:
    f.write(content)
