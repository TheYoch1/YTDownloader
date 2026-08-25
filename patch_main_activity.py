with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    text = f.read()

old_oncreate = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: DownloaderViewModel = viewModel()"""

new_oncreate = """    private lateinit var downloaderViewModel: DownloaderViewModel

    override fun onStop() {
        super.onStop()
        if (::downloaderViewModel.isInitialized) {
            downloaderViewModel.saveQueue()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            val viewModel: DownloaderViewModel = viewModel()
            this.downloaderViewModel = viewModel"""

text = text.replace(old_oncreate, new_oncreate)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(text)
