export const CITIES = [
  "Lahore",
  "Karachi",
  "Islamabad",
  "Rawalpindi",
  "Peshawar",
  "Quetta",
  "Multan",
  "Faisalabad",
];

export const CONSULTATION_TYPES = [
  { label: "Any", value: "" },
  { label: "Online", value: "online" },
  { label: "Physical", value: "physical" },
  { label: "Both", value: "both" },
];

export const BOOKING_CONSULTATION_TYPES = [
  { label: "Online", value: "online" },
  { label: "Physical", value: "physical" },
];

export const DEMO_DOCTOR_ID = 1;

export const SAFETY_NOTE =
  "Smart Doctor Connect AI helps patients find suitable doctors. It does not provide diagnosis, prescriptions, or emergency medical care.";

export const STATUS_COLORS: Record<string, string> = {
  pending: "bg-amber-100 text-amber-800",
  confirmed: "bg-green-100 text-green-800",
  cancelled: "bg-red-100 text-red-800",
  completed: "bg-blue-100 text-blue-800",
  new: "bg-purple-100 text-purple-800",
  contacted: "bg-indigo-100 text-indigo-800",
  closed: "bg-gray-100 text-gray-700",
};
