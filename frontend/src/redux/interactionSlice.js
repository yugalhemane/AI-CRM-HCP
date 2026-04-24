import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: "",
  time: "",
  attendees: "",
  topics: "",
  sentiment: "",
  materials: "",
  samples_distributed: "",
  outcomes: "",
  follow_up_actions: ""
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    updateForm: (state, action) => {
      return { ...state, ...action.payload };
    },
    resetForm: () => initialState
  }
});

export const { updateForm, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;