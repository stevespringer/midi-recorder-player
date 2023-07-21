import os

# Get the total number of tracks in the project
num_tracks = RPR_CountTracks(0)

# Iterate through each track in reverse order
for i in range(num_tracks - 1, -1, -1):
    track = RPR_GetTrack(-1, i)
    # Delete the track
    RPR_DeleteTrack(track)

directory = r"C:\Users\steve\Downloads\macminimidi\reaperdownloads"

# Get the list of files in the directory
files = os.listdir(directory)

# Sort the files in reverse order
files.sort(reverse=True)

# Iterate through each file in reverse order
for filename in files:
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath):
        # Call the RPR_InsertMedia function with the file path
        RPR_InsertMedia(filepath, 1)  # Replace with the actual function call

# Get the first track in the project
track = RPR_GetTrack(0, 0)

# Set the solo state of the track to solo (1)
RPR_SetMediaTrackInfo_Value(track, "I_SOLO", 1)
