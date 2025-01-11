import { useState } from 'react';

export const useVideoFetch = () => {
  //declaring variables needed 
  const [videoLoading, setVideoLoading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState('');
//declaring the function to get the generated video
  const fetchVideoForSong = async (songName, artistName) => {
    try {
      setVideoLoading(true);//sets the loading to true for our circular progress
      
      const url = `https://2a0a-188-141-96-109.ngrok-free.app/song/?song_name=${encodeURIComponent(songName)}&artist_name=${encodeURIComponent(artistName)}`;
      
      //respone with the headers we require
      const response = await fetch(url, { 
        method: 'GET',
        headers: {
          'Accept': 'video/mp4;charset=UTF-8',
          'Accept-Ranges': 'bytes',
          'ngrok-skip-browser-warning': 'true'
        }
      });
// handle the cases where the request isnt successful
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
      }
//converting the response data into a blob to create a video file
      const blob = await response.blob();
      const fileUrl = URL.createObjectURL(blob);// making a url for the video file
//updating the necessary varibles   
      setDownloadUrl(fileUrl);
      setVideoUrl(fileUrl);
      setUploadComplete(true);
// return the file and the complete status
      return { fileUrl, uploadComplete: true };
    } catch (error) {
      console.error('Fetch error:', error);// log the error
      alert(`Error: ${error.message}`);// send an alert to the user with the error
      return { error };
    } finally {
      setVideoLoading(false);// set loading back to false
    }
  };

  //function to handle downloading a file
  const handleDownload = (songName, artistName) => {
    const link = document.createElement('a');// create a temporary anchor element
    link.href = downloadUrl;//set the href to the downloadable URL
    link.setAttribute('download', `${songName}-${artistName}.mp4`);// set the name of the file
    document.body.appendChild(link);//append the link to the DOM
    link.click();//trigger download
    link.remove();//remove the link from the DOM after the download starts
    setUploadComplete(false);// reset upload complete 
  };
  // Function to handle closing the modal 
  const handleCloseModal = () => {
    setUploadComplete(false); // reset upload complete state
    setVideoUrl(null); // clear the video URL
  };
 // returning the variables and functions
  return {
    videoLoading,
    uploadComplete,
    videoUrl,
    fetchVideoForSong,
    handleDownload,
    handleCloseModal
  };
};