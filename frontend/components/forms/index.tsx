// AI-Verify Frontend — Form Components
'use client';

import { useState } from 'react';

export function CompanyForm({ formData, onChange, errors }) {
  const sectors = [
    { value: 'aerospace', label: 'Aerospace & Defense' },
    { value: 'automotive', label: 'Automotive' },
    { value: 'banking', label: 'Banking & Finance' },
    { value: 'education', label: 'Education' },
    { value: 'healthcare', label: 'Healthcare & Pharma' },
    { value: 'retail', label: 'Retail & E-commerce' },
    { value: 'technology', label: 'Technology & SaaS' },
    { value: 'other', label: 'Other' }
  ];

  const revenues = [
    { value: '< €1M', label: '< €1M' },
    { value: '€1M – €10M', label: '€1M – €10M' },
    { value: '€10M – €50M', label: '€10M – €50M' },
    { value: '€50M – €250M', label: '€50M – €250M' },
    { value: '> €250M', label: '> €250M' },
    { value: 'Prefer not to say', label: 'Prefer not to say' }
  ];

  const countries = ['Austria', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 'Belgium', 'Poland', 'Romania', 'Sweden'];

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">Basic Information</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input
            label="Company Size"
            type="select"
            value={formData.company_size}
            onChange={(v) => onChange({ ...formData, company_size: v })}
            options={['Startup (1-10)', 'SME (11-250)', 'Mid-sized (251-1000)', 'Enterprise (1000+)']}
            error={errors.company_size}
          />

          <Input
            label="Sector / Industry"
            type="select"
            value={formData.sector}
            onChange={(v) => onChange({ ...formData, sector: v })}
            options={sectors.map(s => s.label)}
            error={errors.sector}
          />

          <Input
            label="Annual Revenue"
            type="select"
            value={formData.annual_revenue}
            onChange={(v) => onChange({ ...formData, annual_revenue: v })}
            options={revenues.map(r => r.label)}
            error={errors.annual_revenue}
          />

          <Input
            label="Country"
            type="select"
            value={formData.country}
            onChange={(v) => onChange({ ...formData, country: v })}
            options={countries}
            error={errors.country}
          />

          <div className="md:col-span-2">
            <Input
              label="Website URL"
              type="url"
              value={formData.url}
              onChange={(v) => onChange({ ...formData, url: v })}
              placeholder="https://example.com"
              error={errors.url}
            />
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          onClick={() => console.log('Next step')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Next → AI Systems
        </button>
      </div>
    </div>
  );
}

export function AIDetailsForm({ formData, onChange, errors }) {
  const [aiSystemsCount, setAiSystemsCount] = useState(0);

  const handleAiSystemsCountChange = (value) => {
    setAiSystemsCount(value);
    onChange({ ...formData, ai_systems_count: value });
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-50 p-6 rounded-lg">
        <h3 className="text-lg font-semibold mb-4">AI System Details</h3>

        <Input
          label="Number of AI Systems in Production"
          type="select"
          value={formData.ai_systems_count || ''}
          onChange={handleAiSystemsCountChange}
          options={['None yet', '1-3 systems', '4-10 systems', 'More than 10']}
          error={errors.ai_systems_count}
        />

        <Input
          label="Deployment Type"
          type="select"
          value={formData.deployment_type}
          onChange={(v) => onChange({ ...formData, deployment_type: v })}
          options={['Internal use only', 'Customer-facing', 'Both internal and external', 'Third-party AI audit']}
        />

        <Input
          label="Decision Type"
          type="select"
          value={formData.decision_type}
          onChange={(v) => onChange({ ...formData, decision_type: v })}
          options={['Fully automated decisions', 'Human-in-the-loop', 'Decision support only', 'Recommendation only']}
        />

        <Input
          label="Risk Self-Assessment"
          type="select"
          value={formData.risk_self_assessment}
          onChange={(v) => onChange({ ...formData, risk_self_assessment: v })}
          options={['Minimal risk', 'Limited risk', 'High risk', 'Unacceptable risk', 'Not sure']}
        />

        {aiSystemsCount > 0 && (
          <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
            <p className="text-yellow-800 font-medium">⚠️ High-Risk Category Assessment</p>
            <p className="text-yellow-700 text-sm mt-1">If your AI systems affect health, safety, or fundamental rights, they may be classified as high-risk under EU AI Act.</p>
          </div>
        )}
      </div>

      <div className="flex justify-between">
        <button
          onClick={() => onChange({ ...formData, currentStep: 1 })}
          className="px-6 py-3 text-gray-600 hover:text-gray-800"
        >
          ← Back
        </button>
        <button
          onClick={() => console.log('Next step')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Next → Review
        </button>
      </div>
    </div>
  );
}

export function Preview({ formData }) {
  return (
    <div className="bg-gray-50 p-6 rounded-lg">
      <h3 className="text-lg font-semibold mb-4">Review Your Submission</h3>
      <div className="space-y-4 text-sm">
        <div><strong>Company Size:</strong> {formData.company_size || 'Not selected'}</div>
        <div><strong>Sector:</strong> {formData.sector || 'Not selected'}</div>
        <div><strong>Revenue:</strong> {formData.annual_revenue || 'Not selected'}</div>
        <div><strong>Country:</strong> {formData.country || 'Not selected'}</div>
        <div><strong>Website:</strong> {formData.url || 'Not provided'}</div>
        <div><strong>AI Systems:</strong> {formData.ai_systems_count || 'None yet'}</div>
      </div>
      <p className="mt-4 text-gray-600 text-sm">Please review your answers. Once submitted, you'll receive your EU AI Act compliance analysis.</p>

      <div className="flex justify-between mt-6">
        <button
          onClick={() => console.log('Back')}
          className="px-6 py-3 text-gray-600 hover:text-gray-800"
        >
          ← Back
        </button>
        <button
          onClick={() => console.log('Submit')}
          className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          Submit Analysis
        </button>
      </div>
    </div>
  );
}

// Reusable Input Component
function Input({ label, type, value, onChange, options, placeholder, error }) {
  if (type === 'select') {
    return (
      <div className="space-y-2">
        <label className="font-medium">{label}</label>
        <div className="relative">
          <select
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
          >
            <option value="">{`Select ${label.replace(/\d+\./g, '').trim()}...`}</option>
            {options?.map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        </div>
        {error && <p className="text-red-500 text-sm">{error}</p>}
      </div>
    );
  }

  return (
    <div className="space-y-2">
      <label className="font-medium">{label}</label>
      <input
        type={type}
        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  );
}
