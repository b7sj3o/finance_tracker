import { useState } from "react";

const ExampleInsightComponent = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  const toggleModal = () => {
    if (!isModalOpen) {
      setIsModalOpen(true);
      setTimeout(() => setIsVisible(true), 10); // Невелика затримка для плавної появи
    } else {
      setIsVisible(false);
      setTimeout(() => setIsModalOpen(false), 300); // Плавне закриття через 300 мс
    }
  };

  return (
    <>
      <section className="max-w-md mx-auto bg-white rounded-lg p-4">
        {/* Today */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Today</h2>
          <a href="#" className="text-sm text-black">
            See All
          </a>
        </div>

        {/* Item 1 */}
        <article>
          <button
            className="w-full flex items-center justify-between mb-4 p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onClick={toggleModal}
          >
            <div className="flex items-center">
              <div className="bg-blue-100 p-2 rounded-full">
                <svg
                  className="w-6 h-6 text-blue-500"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zm0-18c4.418 0 8 3.582 8 8s-3.582 8-8-8-8-3.582-8-8 3.582-8 8-8zm-2 10h4v2h-4v-2zm1-8v6h2V6h-2z" />
                </svg>
              </div>
              <div className="ml-3 text-left">
                <p className="text-sm font-medium">Bills</p>
                <p className="text-xs text-gray-500">27 July 2024 10:40 AM</p>
              </div>
            </div>
            <div className="text-black font-bold">-$200</div>
          </button>
        </article>

        <hr className="mb-4" />

        {/* Item 2 */}
        <article>
          <button className="w-full flex items-center justify-between mb-4 p-2 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <div className="flex items-center">
              <div className="bg-blue-100 p-2 rounded-full">
                <svg
                  className="w-6 h-6 text-orange-500"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zm0-18c4.418 0 8 3.582 8 8s-3.582 8-8 8-8-3.582-8-8 3.582-8 8-8zm-3 9h6v2H9v-2zm1 2h4v2h-4v-2zm-3 0h6v2H7v-2z" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium">Foods & Drinks</p>
                <p className="text-xs text-gray-500">27 July 2024 1:20 PM</p>
              </div>
            </div>
            <div className="text-black font-bold">-$12</div>
          </button>
        </article>

        {/* Yesterday */}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold">Yesterday</h2>
        </div>
      </section>

      {/* Modal */}
      {isModalOpen && (
        <section>
          {/* Backdrop */}
          <div
            className={`fixed inset-0 bg-black bg-opacity-50 z-40 transition-opacity duration-300 backdrop-blur-sm bg-white/40 ${
              isVisible ? "opacity-100" : "opacity-0"
            }`}
            onClick={toggleModal}
          ></div>

          {/* Modal Window */}
          <div className="fixed inset-0 flex items-center justify-center z-50 mx-4">
            <div
              className={`bg-white p-8 rounded-2xl border-0 shadow-lg max-w-md w-full transition-transform transform duration-1000 ${
                isVisible
                  ? "translate-y-0 opacity-100"
                  : "translate-y-8 opacity-0"
              }`}
            >
              {/* Close Button */}
              <button
                className="absolute top-4 right-4 grayscale hover:grayscale-0 transition-transform duration-300 transform hover:scale-110"
                onClick={toggleModal}
              >
                <svg
                  className="w-6 h-6"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M18.3 5.71a1 1 0 00-1.42 0L12 10.59 7.12 5.71a1 1 0 00-1.42 1.42L10.59 12l-4.88 4.88a1 1 0 001.42 1.42L12 13.41l4.88 4.88a1 1 0 001.42-1.42L13.41 12l4.88-4.88a1 1 0 000-1.42z" />
                </svg>
              </button>

              <h2 className="text-2xl font-semibold mb-4">Name</h2>
              <p className="text-base leading-6 mb-2">expense description</p>
              <p className="text-base leading-6">27 July 2024 10:40 AM</p>
            </div>
          </div>
        </section>
      )}
    </>
  );
};

export default ExampleInsightComponent;
