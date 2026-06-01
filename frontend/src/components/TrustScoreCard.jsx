import React from 'react';

export const TrustScoreCard = ({ trustScore, riskLevel, warnings }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getRiskLevelColor = (level) => {
    const colors = {
      'low': 'text-green-600',
      'medium': 'text-yellow-600',
      'high': 'text-orange-600',
      'critical': 'text-red-600'
    };
    return colors[level] || 'text-gray-600';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-semibold mb-4">Trust Score Analysis</h3>
      
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <span className="text-gray-600">Trust Score:</span>
          <span className={`text-3xl font-bold ${getScoreColor(trustScore)} text-white px-4 py-2 rounded`}>
            {trustScore}%
          </span>
        </div>
      </div>

      <div className="mb-6">
        <span className="text-gray-600">Risk Level:</span>
        <span className={`ml-2 text-lg font-semibold ${getRiskLevelColor(riskLevel)}`}>
          {riskLevel.toUpperCase()}
        </span>
      </div>

      {warnings && warnings.length > 0 && (
        <div className="bg-red-50 border border-red-200 p-4 rounded">
          <h4 className="font-semibold text-red-800 mb-2">Warnings:</h4>
          <ul className="space-y-1">
            {warnings.map((warning, idx) => (
              <li key={idx} className="text-red-700 text-sm">• {warning}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default TrustScoreCard;
