package com.aistudio.ytdownloader

import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

object DownloadRepository {
    private val _downloadQueue = MutableStateFlow<List<QueuedDownload>>(emptyList())
    val downloadQueue: StateFlow<List<QueuedDownload>> = _downloadQueue.asStateFlow()
    
    var appConfig: AppConfig = AppConfig()

    fun updateQueue(updateBlock: (List<QueuedDownload>) -> List<QueuedDownload>) {
        _downloadQueue.update(updateBlock)
    }

    fun addDownload(download: QueuedDownload) {
        _downloadQueue.update { it + download }
    }
    
    fun getDownload(id: String): QueuedDownload? {
        return _downloadQueue.value.find { it.id == id }
    }
}
