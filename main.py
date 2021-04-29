import runner


def main():
    print('Masukkan lokasi file ekspor:')
    # exp_location = input()
    try:
        # runner.get_data(location=exp_location)
        success = runner.push_data('wpxr')  # input
        print(success)
        # print(f'Berhasil diekspor ke {exp_location}')

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
