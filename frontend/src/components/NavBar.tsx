import { graphAnalyticsIcon, homeIcon, transactionIcon, userProfileIcon } from '../assets/images';

const NavBar: React.FC = () => {
    return (
    <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
        <ul className="flex justify-between px-4 py-2">
            <li className="flex flex-col items-center">
                <button className="flex flex-col items-center text-center space-y-1">
                    <img src={homeIcon} alt="Insight" className="w-6 h-6" />
                    <span className="text-xs text-black">Home</span>
                </button>
            </li>
            <li className="flex flex-col items-center">
                <button className="flex flex-col items-center text-center space-y-1">
                    <img src={graphAnalyticsIcon} alt="Insight" className="w-6 h-6" />
                    <span className="text-xs text-gray-500">Insight</span>
                </button>
            </li>
            <li className="flex items-center justify-center">
                <button className="flex items-center justify-center bg-black rounded-full p-2">
                    <svg className="w-6 h-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                    </svg>
                </button>
            </li>
            <li className="flex flex-col items-center">
                <button className="flex flex-col items-center text-center space-y-1">
                    <img src={transactionIcon} alt="Insight" className="w-6 h-6" />
                    <span className="text-xs text-gray-500">Finance</span>
                </button>
            </li>
            <li className="flex flex-col items-center">
                <button className="flex flex-col items-center text-center space-y-1">
                    <img src={userProfileIcon} alt="Insight" className="w-6 h-6" />
                    <span className="text-xs text-gray-500">Profile</span>
                </button>
            </li>
        </ul>
    </nav>
    )
}

export default NavBar