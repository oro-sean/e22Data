def main():
    import pandas as pd
    from datetime import datetime
    import os
    from tkinter.filedialog import askdirectory
    import exifread as ex

    directorypath = askdirectory(initialdir=os.getcwd(), title='Directory with photos')
    filelist = os.listdir(directorypath)

    filepath = os.path.join(directorypath, filelist[0])
    photo = open(filepath, 'rb')
    tags = ex.process_file(photo)
    ts_time = datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S')
    print("The first timestamp is ", ts_time)

    try:
        ts_correct = datetime.strptime(input("Please enter what first time stamp should read"), '%Y-%m-%d %H:%M:%S')

    except:
        ts_correct = ts_time

    ts_delta = ts_correct - ts_time

    dets = []
    counter = 0
    for file in filelist:
        try:
            filepath = os.path.join(directorypath, file)
            photo = open(filepath, 'rb')
            tags = ex.process_file(photo)
            timestamp = datetime.strptime(str(tags['EXIF DateTimeOriginal']), '%Y:%m:%d %H:%M:%S') + ts_delta
            dets.append(
                {
                    'date': timestamp.date(),
                    'time': timestamp.time(),
                    'filepath': filepath
                }
            )
            counter = counter + 1
            print(counter)

        except:
            print('Issue with',file)

    dets_df =  pd.DataFrame(dets)

    for i in range(len(dets_df)):
        print('<event date="',dets_df['date'].iloc[i],'" time="',dets_df['time'].iloc[i],'" type="PhotoEvent" attribute="Not Specified" comments="',dets_df['filepath'].iloc[i],'" photopath="',dets_df['filepath'].iloc[i],'" labelalign="Top" />', sep='', file=f)

main()
#%%
