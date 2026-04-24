import InteractionForm from "./InteractionForm";
import ChatPanel from "./ChatPanel";

const Layout = () => {
  return (
    <div className="container-fluid px-0 min-vh-100 crm-page">
      <div className="row g-0 min-vh-100">
        <div className="col-12 col-lg-8 col-xl-8 border-end crm-left-panel">
          <InteractionForm />
        </div>
        <div className="col-12 col-lg-4 col-xl-4 crm-right-panel">
          <ChatPanel />
        </div>
      </div>
    </div>
  );
};

export default Layout;