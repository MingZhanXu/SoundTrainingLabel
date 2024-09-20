from recording import Recorder
from sql_commands import SqlCommands

def get_last_file(sql):
    result = sql.select_latest_record()
    if result is not None:
        return result[1]
    return None

def run():
    sql = SqlCommands()
    record = Recorder(start_index=1)
    last_file = get_last_file(sql)
    record.print_msg(last_file)
    while True:
        key = record.get_key()
        last_file = get_last_file(sql)

        if key == 'n':
            record.next_page(last_file)
        elif key == 'p':
            record.previous_page(last_file)
        elif key == 'd':
            last_file = get_last_file(sql)
            if last_file is None:
                record.print_msg(last_file)
                record.print_flush(record.no_data_delete, end="")
                continue

            try:
                record.delete_file(last_file)
                sql.delete_last_record()
                last_file = get_last_file(sql)
                record.print_msg(last_file)
                record.print_flush(record.delete_success, end="")
            except Exception as e:
                try:
                    sql.delete_last_record()
                    last_file = get_last_file(sql)
                except Exception as e:
                    record.print_msg(last_file)
                    record.print_flush(record.delete_error % e, end="")
                    continue
                record.print_msg(last_file)
                record.print_flush(record.delete_error % e, end="")
        elif key == '\x1b':  # ESC key
            record.exit()
            break
        elif key >= "1" and key <="9":
            index = int(key) - int("1")
            if index > len(record.file_name[record.page]) - 1:
                record.print_msg(last_file)
            else:
                # set file information
                seq = record.file_data[record.file_name[record.page][index]]
                file_name = record.file_name[record.page][index]
                save_path = f"page{record.page + 1}/{file_name}"
                # record audio
                record.record_audio(save_path, file_name, seq)
                record.add_file_count(index)
                record.print_msg(last_file)
                record.print_flush(record.finish, end="")
                full_file_path = f"./{save_path}/{file_name}{seq}.wav"
                sql.insert_file_path(full_file_path)
                # reshow the last file
                last_file = sql.select_latest_record()[1]
                record.print_msg(last_file)
                record.print_flush(record.finish, end="")
        else:
            record.print_msg(last_file)
            record.print_flush(record.no_function_key, end="")

if __name__ == "__main__":
    run()
    # record.run()