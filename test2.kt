import com.yausername.ffmpeg.FFmpeg
fun main() {
    val f = FFmpeg.getInstance()
    // print methods
    f.javaClass.methods.forEach { println(it.name) }
}
