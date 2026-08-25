import com.yausername.ffmpeg.FFmpeg

fun main() {
    val methods = FFmpeg::class.java.methods
    methods.forEach { println(it.name) }
}
