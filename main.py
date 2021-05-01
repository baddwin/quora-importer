import os
import runner


def main() -> None:
    default_output = os.path.join(os.getcwd(), 'output')
    print('Masukkan lokasi file ekspor!')
    print('Default [{}]:'.format(default_output))

    try:
        exp_location = input() or default_output
        success = runner.process_data('wpxr', exp_location)  # input
        if success:
            print(f'Berhasil diekspor ke {exp_location}')

    except KeyboardInterrupt:
        print('Batal')

    except Exception as e:
        print(f'error: {e}')


if __name__ == "__main__":
    main()
