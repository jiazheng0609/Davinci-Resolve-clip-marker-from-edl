import sys
import os

print("Python version", sys.version)
sys.path.append("C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules")
#sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
import DaVinciResolveScript as dvr_script

sys.path.append("C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts\Comp")
from edl import Parser

try:
    #resolve = dvr_script.scriptapp("Resolve")
    resolve =  app.GetResolve()
    pm = resolve.GetProjectManager()
    proj = pm.GetCurrentProject()
    tl = proj.GetCurrentTimeline()
    mp = proj.GetMediaPool()
    rootfolder = mp.GetRootFolder()
    rootclips = rootfolder.GetClips()
    ms = resolve.GetMediaStorage()
    folder = mp.GetCurrentFolder()
    clips = folder.GetClips()

except:
    print("Open the script file and copy/paste in DVR Console :)")
    sys.exit()

fps = proj.GetSetting()['timelineFrameRate']

def edlExist(mediaFilePath):
    # check if .edl file with same filename exists in same path as audio file
    edlPath = os.path.splitext(mediaFilePath)[0] + '.edl'
    print("finding", edlPath, os.path.exists(edlPath))
    return os.path.exists(edlPath)
        
def getMarkersFromEdl(filepath):
    parser=Parser(fps)
    markerList = []
   
    with open(os.path.splitext(filepath)[0] + '.edl') as f:
        edl = parser.parse(f)

    for event in edl.events:
        frameNum = event.src_start_tc.frame_number
        color = 'Blue' # Default color
        if (event.comments):
            if (event.comments[0] == 'ResolveColorBlue'):
                color = 'Blue'
            elif (event.comments[0] == 'ResolveColorRed'):
                color = 'Red'
            elif (event.comments[0] == 'ResolveColorCyan'):
                color = 'Cyan'
            elif (event.comments[0] == 'ResolveColorGreen'):
                color = 'Green'
            elif (event.comments[0] == 'ResolveColorYellow'):
                color = 'Yellow'
            elif (event.comments[0] == 'ResolveColorPink'):
                color = 'Pink'
            elif (event.comments[0] == 'ResolveColorFuchsia'):
                color = 'Fuchsia'
            elif (event.comments[0] == 'ResolveColorLavender'):
                color = 'Lavender'
            elif (event.comments[0] == 'ResolveColorMint'):
                color = 'Mint'
            elif (event.comments[0] == 'ResolveColorSand'):
                color = 'Sand'
            elif (event.comments[0] == 'ResolveColorCream'):
                color = 'Cream'
        
        markerList.append({'frameNum': frameNum, 'color': color})
    return markerList
        
def addMarkerToClip(markerList, clip):
    x = 0
    #clip.DeleteMarkersByColor('Blue')
    for marker in markerList:
        x+=1
        clip.AddMarker(marker['frameNum'], marker['color'], 'Mark {}'.format(x),  '', 1.0)

# Add marker in project's MediaPool
for clipid in clips:
    clipPath = clips[clipid].GetClipProperty('File Path')
    if (clipPath):
        print("clips " + clipPath)
        if (edlExist(clipPath)):
            markerList = getMarkersFromEdl(clipPath)
            addMarkerToClip(markerList, clips[clipid])
        else:
            print(".edl for {} doesn't exist".format(clipPath))
        
    
# Add marker in every track in current opening timeline
if (tl):
    trackCount = tl.GetTrackCount('audio')
    for track in range(1,trackCount+1):    
        items = tl.GetItemsInTrack("audio", track) 
        for itemId in items:
            poolItem = items[itemId].GetMediaPoolItem()
            piProp = poolItem.GetClipProperty()
            if 'File Path' in piProp:
                filepath = piProp['File Path']
                print("timeline item " + filepath)
                if (edlExist(filepath)):
                    markerList = getMarkersFromEdl(filepath)
                    addMarkerToClip(markerList, items[itemId])
                else:
                    print(".edl for {} doesn't exist".format(filepath))


print()
print('End of script')