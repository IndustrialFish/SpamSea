from csv import writer



for x in range(25000):

    url = "https://opensea.io/collection/" + str(x)

    with open('url-main.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        row = [url]
        csv_writer.writerow(row)

with open('url-main.csv') as fp:
    line = fp.readlines()

for z in range(25000):



    with open('url-main.csv', 'a', newline='') as write_obj:
        csv_writer = writer(write_obj)
        row = [url]
        csv_writer.writerow(row)


