# function that extracts the txt file data
def extract_data(file_number):
    f = open(f'tables/{file_number}.txt', 'r')
    return f.read()