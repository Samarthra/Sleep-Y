'use client';
import { useState } from 'react';
import Link from 'next/link'; // Import Link from Next.js for navigation
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"

export default function Home() {
  const [pdfFile, setPdfFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setPdfFile(file);
    // Call Flask endpoint to start drowsy detection
    fetch('http://localhost:5000/start_detection', {
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Drowsy detection started:', data);
      })
      .catch((error) => console.error('Error starting drowsy detection:', error));
  };

  const stopDetection = () => {
    // Call Flask endpoint to stop drowsy detection
    fetch('http://localhost:5000/stop_detection', {
      method: 'GET',
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Drowsy detection stopped:', data);
        setPdfFile(null); // Reset pdfFile state to null
      })
      .catch((error) => console.error('Error stopping drowsy detection:', error));
  };

  return (
    <div style={{ backgroundImage: `url('./bg1.jpg')`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat', height: '100vh' }}>
      <h1 >Sleep-y</h1>
      
      <div className="container grid w-full max-w-sm items-center gap-1.5 p-20">
      <Label htmlFor="picture">Upload the pdf</Label>
      <Input accept=".pdf" onChange={handleFileChange} id="picture" type="file" />

      <Button onClick={stopDetection}>Stop Detection</Button>
    </div>
      {pdfFile && (
        <iframe
        title="PDF Viewer"
        src={URL.createObjectURL(pdfFile)}
        width="100%"
        height="800px"
        ></iframe>
      )}
 

 
  
    </div>
  );
}
