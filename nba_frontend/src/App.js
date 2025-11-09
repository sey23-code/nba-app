import TeamsList from './TeamsList';
import {Routes, Route } from "react-router-dom"
import RosterList from './RosterList';
import PlayerStats from './PlayerStats';
import PlayerComparisonPage from './PlayerComparisonPage';
import TodayMatchups from './TodayMatchups';
import './App.css';
function App() {
  return (
    <Routes>
      <Route path="/" element={<TeamsList />}/>
      <Route path="/team/:teamId" element={<RosterList />}/>
      <Route path="/player/:playerId" element={<PlayerStats />}></Route>
      <Route path="/compare" element={<PlayerComparisonPage />}></Route>
      <Route path="/games/today" element={<TodayMatchups />}></Route>
    </Routes>
  );
}

export default App;
