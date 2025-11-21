import { Outlet } from 'react-router-dom'
import './AppShell.css'
import TopBar from './TopBar'

function AppShell() {
  return (
    <div className="app-shell">
      <div className="main-content">
        <TopBar />
        <main className="content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppShell
