package com.aistudio.ytdownloader
import com.yausername.youtubedl_android.mapper.VideoFormat
class TestClass {
    fun test(v: VideoFormat) {
        val size = v.fileSize
        val e = v.ext
        val vcodec = v.vcodec
        val acodec = v.acodec
    }
}
