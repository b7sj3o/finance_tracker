import React, { useState } from "react";

type TransactionType = "income" | "expenses";

const TransactionToggle: React.FC = () => {
  const [selectedType, setSelectedType] = useState<TransactionType>("income");

  return (
    <div className="container mx-auto p-7">
      <h2 className="transaction__header text-center font-bold mb-7">Add New</h2>
      <div className="flex flex-col items-center">
      <div className="flex bg-gray-200 rounded-full p-1">
        <button
          className={`px-4 py-2 rounded-full ${
            selectedType === "income" ? "bg-black text-white" : "text-black"
          }`}
          onClick={() => setSelectedType("income")}
        >
          Income
        </button>
        <button
          className={`px-4 py-2 rounded-full ${
            selectedType === "expenses" ? "bg-black text-white" : "text-black"
          }`}
          onClick={() => setSelectedType("expenses")}
        >
          Expenses
        </button>
      </div>
    </div>
    </div>
  );
};

export default TransactionToggle;
