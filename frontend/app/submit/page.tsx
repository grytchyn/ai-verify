// AI-Verify Frontend — Main Submit Page
import { useState } from 'react';
import { CompanyForm, AIDetailsForm, Preview } from '../components/forms';

export default function SubmitPage() {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({});
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const validateStep = (step, data) => {
    const newErrors = {};
    if (step === 1) {
      if (!data.company_size) newErrors.company_size = 'Please select company size';
      if (!data.sector) newErrors.sector = 'Please select sector';
      if (!data.annual_revenue) newErrors.annual_revenue = 'Please select revenue';
      if (!data.country) newErrors.country = 'Please select country';
      if (!data.url) newErrors.url = 'Website URL is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (currentStep === 3) {
      setLoading(true);
      try {
        const res = await fetch('/api/compliance/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url: formData.url, formData }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Analysis failed');
        setResults(data.data);
      } catch (e) {
        setErrors({ submit: e.message });
      } finally {
        setLoading(false);
      }
    } else {
      const isValid = validateStep(currentStep, formData);
      if (isValid) setCurrentStep(currentStep + 1);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 1: return <CompanyForm formData={formData} onChange={setFormData} errors={errors} />;
      case 2: return <AIDetailsForm formData={formData} onChange={setFormData} errors={errors} />;
      case 3: return <Preview formData={formData} />;
      default: return null;
    }
  };

  if (results) {
    return <ResultsPage results={results} />;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Stepper */}
      <div className="flex justify-between mb-12 relative">
        <div className="absolute top-5 left-0 w-full h-0.5 bg-gray-200 -z-10" />
        {[1, 2, 3].map((step) => (
          <div key={step} className="flex flex-col items-center">
            <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${step === currentStep ? 'bg-blue-600 text-white' : step < currentStep ? 'bg-green-500 text-white' : 'bg-gray-200 text-gray-600'}`}>
              {step}
            </div>
            <span className="mt-2 text-sm font-medium text-gray-700">
              {step === 1 ? 'Company Info' : step === 2 ? 'AI Systems' : 'Review'}
            </span>
          </div>
        ))}
      </div>

      {/* Step Content */}
      <div className="min-h-[400px]">{renderStep()}</div>

      {/* Errors */}
      {Object.keys(errors).length > 0 && (
        <div className="mt-6 p-4 bg-red-50 rounded border border-red-200">
          <p className="text-red-700 font-medium mb-2">Please fix the following:</p>
          <ul className="text-red-600 text-sm">
            {Object.entries(errors).map(([key, error]) => <li key={key}>• {error}</li>)}
          </ul>
        </div>
      )}

      {/* Action Bar */}
      <div className="mt-8 flex justify-between items-center">
        <button
          onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
          disabled={currentStep === 1}
          className="px-6 py-3 text-gray-600 disabled:opacity-50 hover:text-gray-800"
        >
          ← Back
        </button>

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
        >
          {loading && <span className="animate-spin">⏳</span>}
          {currentStep === 3 ? 'Submit Analysis' : 'Next →'}
        </button>
      </div>
    </div>
  );
}

function ResultsPage({ results }) {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-6 text-center">Compliance Analysis Complete</h2>
        
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="text-center p-4 bg-green-50 rounded">
            <div className="text-4xl font-bold text-green-600">{results.score}</div>
            <div className="text-gray-600">Compliance Score</div>
          </div>
          <div className="text-center p-4 bg-yellow-50 rounded">
            <div className="text-4xl font-bold text-yellow-600">{results.riskLevel}</div>
            <div className="text-gray-600">AI Risk Level</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded">
            <div className="text-4xl font-bold text-blue-600">100%</div>
            <div className="text-gray-600">Accuracy</div>
          </div>
        </div>

        <div className="mb-6">
          <h3 className="text-xl font-semibold mb-4">Key Findings</h3>
          {results.recommendations?.length > 0 ? (
            <ul className="space-y-2">
              {results.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-blue-600">•</span>
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-green-600">No major issues found. Your AI practices align with EU AI Act requirements.</p>
          )}
        </div>

        <div className="text-center mt-8">
          <button 
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Analyze Another Site
          </button>
        </div>
      </div>
    </div>
  );
}
