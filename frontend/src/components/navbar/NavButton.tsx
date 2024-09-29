import React from "react";
import { useNavigate } from "react-router-dom";

interface NavButtonProps {
  icon: string;
  path: string;
  label?: string;
  isActive?: boolean;
  onClick?: () => void;
}

const NavButton: React.FC<NavButtonProps> = ({
  icon,
  label,
  path,
  isActive = false,
}) => {
  const navigate = useNavigate();

  return (
    <li className="flex flex-col items-center">
      <button
        className={`flex flex-col items-center text-center space-y-1 ${
          isActive ? "text-black" : "text-gray-500"
        }`}
        onClick={() => navigate(path)}
      >
        <img src={icon} alt={label || "icon"} className="w-6 h-6" />
        {label && <span className="text-xs">{label}</span>}
      </button>
    </li>
  );
};

export default NavButton;
