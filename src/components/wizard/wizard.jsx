import React, { useState } from 'react';
import Step1 from './Step1';
import Step2 from './Step2';
import StepSummary from './StepSummary';

const Wizard = () => {
    const [step, setStep] = useState(1);
    const [formData, setFormData] = useState({
        projectName: '',
        description: '',
    });

    const nextStep = () => setStep((prevStep) => prevStep + 1);
    const previousStep = () => setStep((prevStep) => prevStep - 1);

    return (
        <div className="wizard">
            {step === 1 && <Step1 formData={formData} setFormData={setFormData} nextStep={nextStep} />}
            {step === 2 && <Step2 formData={formData} setFormData={setFormData} nextStep={nextStep} previousStep={previousStep} />}
            {step === 3 && <StepSummary formData={formData} previousStep={previousStep} />}
        </div>
    );
};

export default Wizard;
