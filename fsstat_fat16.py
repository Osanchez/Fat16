import struct

# Helper functions 'as_le_unsigned' and 'get_cluster_numbers' were gathered from course website lecture notes
# http://people.cs.umass.edu/~liberato/courses/2018-spring-compsci365+590f/lecture-notes/12-demonstration-parsing-fat/


def as_le_unsigned(b):
    table = {1: 'B', 2: 'H', 4: 'L', 8: 'Q'}
    return struct.unpack('<' + table[len(b)], b)[0]


def get_cluster_numbers(first_cluster, fat_bytes, cluster_size):
    result = [first_cluster]
    offset = 2 * first_cluster
    next_cluster = as_le_unsigned(fat_bytes[offset:offset + 2])
    while next_cluster < as_le_unsigned(b'\xf8\xff'):
        result.append(next_cluster)
        offset = 2 * next_cluster
        next_cluster = as_le_unsigned(fat_bytes[offset:offset + 2])
    return result


def get_oem_name(b):
    return b[3:11].decode('ascii').strip()


def get_volume_id(b):
    return hex(as_le_unsigned(b[39:43]))


def get_volume_label(b):
    return b[43:54].decode('ascii').strip()


def get_filesystem_type(b):
    return b[54:62].decode('ascii').strip()


def get_sectors_start(b):
    return as_le_unsigned(b[28:32])


def get_sector_count(b):
    return max(as_le_unsigned(b[19:21]), as_le_unsigned(b[32:36])) - 1


def get_reserved_area_size(b):
    return as_le_unsigned(b[14:16])


def get_fat_size(b):
    return  as_le_unsigned(b[22:24])


def get_fat_start(b, offset):  # TODO: Make sure function calls take offset parameter
    return get_sectors_start(b) - offset + 1


def get_number_fats(b):
    return as_le_unsigned(b[16:17])


def fsstat_fat16(fat16_file, sector_size=512, offset=0):
    result = ['FILE SYSTEM INFORMATION',
              '--------------------------------------------',
              'File System Type: FAT16',
              '']

    # then do a few things, .append()ing to result as needed... Maybe that's a hint hmmmmm
    fat16_file.seek(offset * sector_size)
    boot_sector = fat16_file.read(sector_size)

    fat16_file.seek(offset*sector_size)
    boot_sector = fat16_file.read(sector_size)
    result.append('OEM Name: ' + get_oem_name(boot_sector))
    result.append('Volume ID: ' + get_volume_id(boot_sector))
    result.append('Volume Label (Boot Sector): ' + get_volume_label(boot_sector))
    result.append('File System Type Label: ' + get_filesystem_type(boot_sector))
    result.append('')
    result.append('Sectors before file system: ' + str(get_sectors_start(boot_sector)))
    result.append('')
    result.append('File System Layout (in sectors)')
    result.append('Total Range: ' + str(get_sectors_start(boot_sector) - offset) + ' - ' + str(get_sector_count(boot_sector)))
    result.append('* Reserved: ' + str(get_sectors_start(boot_sector) - offset) + ' - '
                  + str(get_sectors_start(boot_sector) - offset + get_reserved_area_size(boot_sector) - 1))
    result.append('** Boot Sector: ' + str(get_sectors_start(boot_sector) - offset))
    for f in range(get_number_fats(boot_sector)):
        fat_start = get_fat_start(boot_sector, offset)
        fat_size = get_fat_size(boot_sector)
        result.append('* FAT ' + str(f) + ': ' + str(fat_start) + ' - ' + str(fat_start + fat_size - 1))
    # 38

        return result