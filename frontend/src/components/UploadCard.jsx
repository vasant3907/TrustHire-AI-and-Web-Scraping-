import React from 'react';

export const UploadCard = ({ onUpload }) => {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onUpload(file);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">Upload Job Description</h3>
      <div className="border-2 border-dashed border-gray-300 p-8 text-center rounded">
        <p className="text-gray-600 mb-4">Drag & drop or click to upload</p>
        <input
          type="file"
          onChange={handleFileChange}
          className="hidden"
          id="file-upload"
        />
        <label htmlFor="file-upload" className="bg-blue-600 text-white px-4 py-2 rounded cursor-pointer">
          Choose File
        </label>
      </div>
    </div>
  );
};

export default UploadCard;
