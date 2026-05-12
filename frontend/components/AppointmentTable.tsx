import { Appointment } from "@/lib/types";
import { STATUS_COLORS } from "@/lib/constants";

export default function AppointmentTable({ appointments }: { appointments: Appointment[] }) {
  if (!appointments.length) {
    return <p className="text-slate-500 text-sm py-6 text-center">No appointments yet.</p>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-200 text-slate-500">
            <th className="text-left py-3 px-4 font-semibold">Patient</th>
            <th className="text-left py-3 px-4 font-semibold">Contact</th>
            <th className="text-left py-3 px-4 font-semibold">Date</th>
            <th className="text-left py-3 px-4 font-semibold">Time</th>
            <th className="text-left py-3 px-4 font-semibold">Type</th>
            <th className="text-left py-3 px-4 font-semibold">Status</th>
          </tr>
        </thead>
        <tbody>
          {appointments.map((appt) => (
            <tr key={appt.id} className="border-b border-slate-100 hover:bg-slate-50">
              <td className="py-3 px-4 font-medium text-slate-900">{appt.patient_name}</td>
              <td className="py-3 px-4 text-slate-600">{appt.patient_contact}</td>
              <td className="py-3 px-4 text-slate-600">{appt.appointment_date}</td>
              <td className="py-3 px-4 text-slate-600">{appt.appointment_time}</td>
              <td className="py-3 px-4 capitalize text-slate-600">{appt.consultation_type}</td>
              <td className="py-3 px-4">
                <span className={`${STATUS_COLORS[appt.status] || "bg-gray-100 text-gray-700"} text-xs font-semibold px-2 py-1 rounded-full capitalize`}>
                  {appt.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
