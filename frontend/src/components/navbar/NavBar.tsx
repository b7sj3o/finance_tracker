import { Outlet } from "react-router-dom";
import {
  graphAnalyticsIcon,
  homeIcon,
  transactionIcon,
  plusIcon,
  userProfileIcon,
} from "../../assets";
import NavButton from "./NavButton";

const NavBar: React.FC = () => {
  return (
    <>
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
        <ul className="flex justify-between px-4 py-2">
          <NavButton icon={homeIcon} label="Home" path="/" isActive />
          <NavButton
            icon={graphAnalyticsIcon}
            label="Insight"
            path="/insight"
          />
          <NavButton icon={plusIcon} path="/add-transaction"/>
          <NavButton
            icon={transactionIcon}
            label="Finance"
            path="/transactions"
          />
          <NavButton
            icon={userProfileIcon }
            label="Profile"
            path="/insight"
          />
        </ul>
      </nav>
      <Outlet />
    </>
  );
};

export default NavBar;
