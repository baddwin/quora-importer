import os
import runner


def main() -> None:
    default_output = os.path.join(os.getcwd(), 'output')
    default_input = os.path.join(os.getcwd(), 'content')

    try:
        print('Masukkan lokasi data!')
        print('Default [{}]:'.format(default_input))
        con_location = input() or default_input
        print('Masukkan lokasi file hasil ekspor!')
        print('Default [{}]:'.format(default_output))
        exp_location = input() or default_output
        success = runner.process_data('wpxr', con_location, exp_location)  # input
        if success:
            print(f'Berhasil diekspor ke {exp_location}')

    except KeyboardInterrupt:
        print('Batal')

    except Exception as e:
        print(f'error: {e}')


if __name__ == "__main__":
    main()
