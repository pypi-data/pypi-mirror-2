import eyeD3, sys, os, urllib, re

class cddbsearch:
    """
    Simple front-end to the web-interface of CDDB
    
    Create an object by passing it a path to a directory of mp3's. 
    Then call the search function to see if theres a result. 
    If there is a result, an array of dictionaries will be returned. The dictionary holds the genre, cddbid, and title of the results.
    You may return the tracks of a specific result using the getResult function.
    """
   
    total_time = 0
    total_frames = ''
    disc_id = ''
    num_files = 0

    def __init__(self, dir):
        if not os.path.isdir(dir):
            raise IOError("Path does not exist")
        else:
            files = []
            for file in os.listdir(dir):
                (name, ext) = os.path.splitext(file)
                if ext.lower() == '.mp3':
                    files.append(os.path.join(dir, file))

            self.num_files = len(files)
            files.sort()

            n = 0
            for file in files:
                mp3 = eyeD3.Mp3AudioFile(file)
                self.total_frames = self.total_frames + str(self.total_time * 75) + " "
                self.total_time += int(mp3.getPlayTime())
                n += self.cddb_sum(int(mp3.getPlayTime()))
            tmp = ((long(n) % 0xFF) << 24 | self.total_time << 8 | self.num_files)
            self.disc_id = '%08lx' % tmp

    def search(self):
        searchstring = self.disc_id + " " + str(self.num_files) + " " + self.total_frames + str(self.total_time)
        searchstring = searchstring.replace(' ', '+')
        results = urllib.urlopen('http://freedb.freedb.org/~cddb/cddb.cgi?cmd=cddb+query+' + searchstring + '&hello=cddbsearch+localhost+xmcd+2.1&proto=6')
        result = results.readlines()[1:-1]
        f = []
        for i in result:
            genre = i.split(' ')[0]
            cddbid = i.split(' ')[1]
            title = ' '.join(i.split(' ')[2:]).rstrip("\r\n")
            f.append({'genre':genre,'cddbid':cddbid,'title':title})
        return f

    def getResult(self, genre, cddbid):
        tracknames = []
        searchstring = genre + " " + cddbid
        searchstring = searchstring.replace(' ', '+')
        results = urllib.urlopen('http://freedb.freedb.org/~cddb/cddb.cgi?cmd=cddb+read+' + searchstring + '&hello=cddbsearch+localhost+xmcd+2.1&proto=6')
        if results:
            for line in results:
                if re.match(r'^TTITLE',line):
                    trackname = re.sub(r'^TTITLE\d+=','',line)
                    tracknames.append(trackname.rstrip("\n"))
        return tracknames

    def cddb_sum(self, n):
        ret = 0
        while n > 0:
            ret = ret + (n % 10)
            n = n / 10
        return ret
