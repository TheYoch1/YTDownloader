import com.yausername.ffmpeg.FFmpeg;
import java.lang.reflect.Method;

public class TestFFmpeg {
    public static void main(String[] args) {
        for (Method m : FFmpeg.class.getDeclaredMethods()) {
            System.out.println(m.getName());
        }
    }
}
