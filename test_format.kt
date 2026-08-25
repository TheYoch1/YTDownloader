import com.yausername.youtubedl_android.mapper.VideoFormat
import kotlin.reflect.full.memberProperties

fun main() {
    VideoFormat::class.memberProperties.forEach {
        println(it.name)
    }
}
