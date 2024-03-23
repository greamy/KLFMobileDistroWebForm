import os

class DiskUtility:

	def __init__(self):
		pass

	def get_disk_udage(self, path):
		stats = os.statvfs(path)
		total_blocks = stats.f_blocks
		free_blocks = stats.f_bfree
		block_size = stats.f_frsize
		usage_percent = (free_blocks / float(total_blocks)) * 100.0
		remaining_space = free_blocks * block_size
		total_size = total_blocks * block_size
		return usage_percent, self.convert_to_logical_units(total_size), self.convert_to_logical_units(remaining_space)
		# return usage_percent, stats

	def convert_to_logical_units(self, num_bytes):
		units = ["B", "KB", "MB", "GB", "TB", "PB"]
		i = 0
		while num_bytes >= 1024:
			num_bytes /= 1024.
			i += 1
		return num_bytes, units[i]


if __name__ == "__main__":
	disk = DiskUtility()
	print(disk.get_disk_udage("/"))
