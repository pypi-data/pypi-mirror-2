import sys, os, eyeD3
import optparse
from cddb import cddbsearch

def main():

    parser = optparse.OptionParser()
    parser.add_option('-t', '--tag', help='tag results', dest='tag', default=False, action='store_true')
    parser.add_option('-d', '--dir', help='directory of mp3s', dest='dir', default=False, action='store')

    (opts, args) = parser.parse_args()

    if not opts.dir:
        print "A mandatory option is missing\n"
        parser.print_help()
        exit(-1)
    else:
        if os.path.isdir(opts.dir):
            cddb = cddbsearch(opts.dir)
            results = cddb.search()
            print "Found ", len(results), " results for " + cddb.disc_id + ":"
            if len(results):
                for i in results:
                    print "  [" + str(results.index(i) + 1) + "] " + " " + i['cddbid'] + "   " + i['title']

                if opts.tag:
                    choice = int(raw_input("Pick a result (-1 to exit): "))

                    if choice > 0:
                        choice = choice - 1
                        tracks = cddb.getResult(results[choice]['genre'], results[choice]['cddbid'])
                        artist = results[choice]['title'].split(' / ')[0]
                        album  = results[choice]['title'].split(' / ')[1]
                        for track in tracks:
                            print track
                        tag = raw_input("Tag? y/n: ")
                        if tag.lower() == 'y':
                            files = []
                            for file in os.listdir(opts.dir):
                                (name, ext) = os.path.splitext(file)
                                if ext.lower() == '.mp3':
                                    files.append(os.path.join(opts.dir, file))
                            files.sort()
                            x = 0
                            for file in files:
                                mp3 = eyeD3.Tag()
                                mp3.link(file)
                                mp3.setArtist(artist)
                                mp3.setAlbum(album)
                                mp3.setTitle(tracks[x])
                                mp3.setTrackNum((x+1, len(tracks)))
                                mp3.update()
                                x = x + 1

if __name__ == '__main__':
    main()
