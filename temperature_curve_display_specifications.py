import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceArea } from 'recharts';
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { FileUp, RefreshCw, ZoomOut } from "lucide-react";

const TempVizApp = () => {
  const [data, setData] = useState([]);
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Zoom state
  const [leftIndex, setLeftIndex] = useState(null);
  const [rightIndex, setRightIndex] = useState(null);
  const [isZooming, setIsZooming] = useState(false);
  const [zoomedData, setZoomedData] = useState(null);

  // Function to handle file reading
  const readFileContent = async (file) => {
    setIsLoading(true);
    setError(null);
    try {
      const text = await file.text();
      return text;
    } catch (error) {
      console.error('Error reading file:', error);
      setError(`Error reading file: ${error.message}`);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const parseTemperatureLog = (text) => {
    const lines = text.split('\n');
    const parsedData = [];

    lines.forEach((line, index) => {
      if (!line.trim()) return;

      try {
        const [timestamp_str, temp_str] = line.trim().split(/\s+/);
        const timestamp = new Date(timestamp_str.replace('_', ' '));
        const temperature = parseFloat(temp_str.split('=')[1].replace('\'C', ''));

        if (!isNaN(temperature) && timestamp instanceof Date && !isNaN(timestamp)) {
          parsedData.push({
            name: timestamp.toLocaleString(),
            temperature: temperature,
            originalIndex: index
          });
        }
      } catch (error) {
        console.warn('Skipping invalid line:', line);
      }
    });

    return parsedData;
  };

  const handleFileSelect = async (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      // Reset all states first
      setData([]);
      setZoomedData(null);
      setError(null);
      setIsLoading(true);
      
      try {
        // Create a new FileReader for each read operation
        const reader = new FileReader();
        const text = await new Promise((resolve, reject) => {
          reader.onload = (e) => resolve(e.target.result);
          reader.onerror = (e) => reject(new Error('File read failed'));
          reader.readAsText(selectedFile);
        });
        
        const parsedData = parseTemperatureLog(text);
        console.log(`Loaded ${parsedData.length} data points`);
        setFile(selectedFile);
        setData(parsedData);
      } catch (error) {
        console.error('Error reading file:', error);
        setError(`Error reading file: ${error.message}`);
      } finally {
        setIsLoading(false);
      }
    }
    // Clear the input value to ensure the change event fires even if selecting the same file
    event.target.value = '';
  };

  const handleRefresh = async () => {
    if (file) {
      try {
        const text = await readFileContent(file);
        const parsedData = parseTemperatureLog(text);
        setData(parsedData);
        setZoomedData(null);
      } catch (error) {
        // Error is already handled in readFileContent
      }
    }
  };

  // ... rest of the component remains the same ...
  const handleMouseDown = (e) => {
    if (e && typeof e.activeTooltipIndex !== 'undefined') {
      setIsZooming(true);
      setLeftIndex(e.activeTooltipIndex);
      setRightIndex(e.activeTooltipIndex);
      console.log('Mouse down at index:', e.activeTooltipIndex); // Debug log
    }
  };

  const handleMouseMove = (e) => {
    if (!isZooming) return;
    
    const currentData = zoomedData ? zoomedData.data : data;
    const newRightIndex = (!e || typeof e.activeTooltipIndex === 'undefined') 
      ? currentData.length - 1 
      : e.activeTooltipIndex;
    
    setRightIndex(newRightIndex);
    console.log('Mouse move, setting right index:', newRightIndex); // Debug log
  };

  const handleMouseUp = () => {
    if (!isZooming) return;
    console.log('Mouse up, indices:', leftIndex, rightIndex); // Debug log
    
    setIsZooming(false);
    
    if (leftIndex === null || rightIndex === null) {
      setLeftIndex(null);
      setRightIndex(null);
      return;
    }

    const currentData = zoomedData ? zoomedData.data : data;
    const start = Math.min(leftIndex, rightIndex);
    const end = Math.max(leftIndex, rightIndex);

    // Only zoom if we have a valid range
    if (start !== end) {
      if (zoomedData) {
        const newStartIndex = currentData[start].originalIndex;
        const newEndIndex = currentData[end].originalIndex;
        const newData = data.filter(point => 
          point.originalIndex >= newStartIndex && 
          point.originalIndex <= newEndIndex
        );
        setZoomedData({
          data: newData,
          startIndex: newStartIndex,
          endIndex: newEndIndex
        });
      } else {
        setZoomedData({
          data: data.slice(start, end + 1),
          startIndex: start,
          endIndex: end
        });
      }
    }

    setLeftIndex(null);
    setRightIndex(null);
  };

  const resetZoom = () => {
    setZoomedData(null);
    setLeftIndex(null);
    setRightIndex(null);
  };

  // Prevent text selection during zoom
  useEffect(() => {
    const preventDefault = (e) => {
      if (isZooming) {
        e.preventDefault();
      }
    };

    document.addEventListener('selectstart', preventDefault);
    return () => document.removeEventListener('selectstart', preventDefault);
  }, [isZooming]);

  const displayData = zoomedData ? zoomedData.data : data;
  const tickInterval = Math.max(1, Math.floor(displayData.length / 10));

  return (
    <div className="p-4">
      <div className="mb-4 flex gap-4">
        <Button 
          onClick={() => document.getElementById('file-input').click()}
          className="flex items-center gap-2"
        >
          <FileUp size={16} />
          Select File
        </Button>
        <input
          type="file"
          id="file-input"
          className="hidden"
          onChange={handleFileSelect}
          accept=".log,.txt"
        />
        <Button
          onClick={resetZoom}
          disabled={!zoomedData}
          className="flex items-center gap-2"
        >
          <ZoomOut size={16} />
          Reset Zoom
        </Button>
      </div>

      {error && (
        <Alert className="mb-4" variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {file && (
        <Alert className="mb-4">
          <AlertDescription>
            File: <strong>{file.name}</strong> ({data.length} data points loaded)
            {zoomedData && ` - Showing ${zoomedData.data.length} points`}
          </AlertDescription>
        </Alert>
      )}

      {displayData.length > 0 && (
        <div style={{ width: '100%', height: '600px', border: '1px solid #ddd', borderRadius: '8px', padding: '16px', userSelect: 'none' }}>
          <ResponsiveContainer>
            <LineChart
              data={displayData}
              margin={{ top: 20, right: 30, left: 60, bottom: 60 }}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45} 
                textAnchor="end"
                height={80}
                interval={tickInterval}
              />
              <YAxis 
                label={{ 
                  value: 'Temperature (°C)', 
                  angle: -90, 
                  position: 'insideLeft',
                  offset: -40
                }}
              />
              <Tooltip />
              <Legend />
              <Line 
                type="monotone" 
                dataKey="temperature" 
                stroke="#ff0000" 
                dot={false} 
                name="Temperature"
                isAnimationActive={false}
              />
              {isZooming && typeof leftIndex === 'number' && displayData && displayData.length > 0 && (
                <ReferenceArea
                  x1={displayData[leftIndex]?.name}
                  x2={displayData[rightIndex ?? leftIndex]?.name}
                  strokeOpacity={0.3}
                  fill="#8884d8"
                  fillOpacity={0.3}
                />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
      
      {!displayData.length && !isLoading && (
        <div className="text-center p-8 text-gray-500 border rounded-lg">
          Select a temperature log file to visualize the data
        </div>
      )}
      
      {isLoading && (
        <div className="text-center p-8 text-gray-500 border rounded-lg">
          Loading data...
        </div>
      )}
    </div>
  );
};

export default TempVizApp;
