import re
with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "r") as f:
    content = f.read()

target1 = '''fun DownloadItemCard(
    download: QueuedDownload,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit
) {'''
rep1 = '''fun DownloadItemCard(
    download: QueuedDownload,
    onRemove: () -> Unit,
    onCancel: () -> Unit,
    onPause: () -> Unit,
    onResume: () -> Unit,
    onRetry: () -> Unit
) {'''
content = content.replace(target1, rep1)

target2 = '''                                DownloadItemCard(
                                    download = download,
                                    onRemove = { viewModel.removeDownload(download.id) },
                                    onCancel = { viewModel.cancelDownload(download.id) },
                                    onPause = { viewModel.pauseDownload(download.id) },
                                    onResume = { viewModel.resumeDownload(download.id) }
                                )'''
rep2 = '''                                DownloadItemCard(
                                    download = download,
                                    onRemove = { viewModel.removeDownload(download.id) },
                                    onCancel = { viewModel.cancelDownload(download.id) },
                                    onPause = { viewModel.pauseDownload(download.id) },
                                    onResume = { viewModel.resumeDownload(download.id) },
                                    onRetry = { viewModel.retryDownload(download.id) }
                                )'''
content = content.replace(target2, rep2)

target3 = '''                    }
                }
            }
        }
    }
}'''

target3 = '''                    }
                }
            }
        }
    }
}'''

target3 = '''                    IconButton(
                        onClick = onCancel,
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            Icons.Default.Stop,
                            contentDescription = "Cancel",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                }'''

rep3 = '''                    IconButton(
                        onClick = onCancel,
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            Icons.Default.Stop,
                            contentDescription = "Cancel",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                } else if (download.status == "Error") {
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(
                        onClick = onRetry,
                        modifier = Modifier.size(24.dp)
                    ) {
                        Icon(
                            Icons.Default.Refresh,
                            contentDescription = "Retry",
                            tint = MaterialTheme.colorScheme.error
                        )
                    }
                }'''

content = content.replace(target3, rep3)

with open("app/src/main/java/com/aistudio/ytdownloader/MainActivity.kt", "w") as f:
    f.write(content)
print("done")
