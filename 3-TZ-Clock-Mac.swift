// //////////////////////////////////////////////////////
//  myWorldClock.swift
//  2026-0309 Converted from Python with help of Gemini.
// //////////////////////////////////////////////////////
import SwiftUI
import Combine
import Foundation

// 1. Ensure this is the ONLY @main in your entire project
@main
struct myWorldClockApp: App {
    var body: some Scene { WindowGroup { ClockView() } } }

struct ClockView: View {
    @State private var currentTime = Date()
    @State private var timeSeoul: String = ""
    @State private var timeSydney: String = ""
    
    private let timeZoneSeoul = TimeZone(identifier: "Asia/Seoul")!
    private let timeZoneSydney = TimeZone(identifier: "Australia/Sydney")!
    
    var body: some View {
        VStack {
            ZStack { // Clock Face
                Circle()
                    .fill(Color.black)
                    .frame(width: 300, height: 300) // Adj size for standard screens
                    .overlay(Circle().stroke(Color(red: 255/255, green: 127/255, blue: 80/255), lineWidth: 4))
                
                // Hour Markers
                ForEach(1..<13) { i in // 12 at the top
                    let angle = Angle(degrees: Double(i) * 30 - 90)
                    let x = 132 * cos(angle.radians)
                    let y = 132 * sin(angle.radians)
                    Text("\(i)")
                        .font(.system(size: 20, weight: .bold))
                        .foregroundColor(.white)
                        .position(x: 150 + CGFloat(x), y: 150 + CGFloat(y))
                }
                
                // Clock Hands - -90 adj to align 0° with 12 o'clock
                ClockHand(length: 76, angle: hourAngle - 90)
                    .stroke(Color.white, style: StrokeStyle(lineWidth: 5, lineCap: .round))
                ClockHand(length: 108, angle: minuteAngle - 90)
                    .stroke(Color.white, style: StrokeStyle(lineWidth: 3, lineCap: .round))
                ClockHand(length: 120, angle: secondAngle - 90)
                    .stroke(Color.yellow, style: StrokeStyle(lineWidth: 2, lineCap: .round))
                
                // Center Point (Magenta)
                Circle()
                    .fill(Color(red: 1.0, green: 0, blue: 1.0))
                    .frame(width: 10, height: 10)
            }
            .frame(width: 300, height: 200)
            .padding(.bottom, 0)
           
            VStack(spacing: 0) {
                Text("\(formYear(currentTime))") // color Wheat
                    .foregroundColor(Color(hex: "#F5DEB3") ?? .blue)
                    .font(.system(size: 20, weight: .bold))
                    .position(x: 64, y: 20)
                Text("\(formDate(currentTime))")
                    .foregroundColor(Color(hex: "#F5DEB3") ?? .blue)
                    .font(.system(size: 20, weight: .bold))
                    .position(x: 330, y: -5)
        // ["LightGreen", "Orange", "Blue", "LightBlue", "SlateBlue", "Tomato", "Tomato"]
                let ClrTbl = ["#FF6347", "#90EE90", "#FFA500", "#0000FF", "#ADD8E6", "#6A5ACD", "#FF6347"]
                let dayIdx = Calendar.current.component(.weekday, from: currentTime) - 1
                let theColor = ClrTbl[dayIdx]
                Text("\(formDoW(currentTime))")
                    .foregroundColor(Color(hex: theColor) ?? .blue)
                    .font(.system(size: 20, weight: .bold))
                    .padding(.bottom, 20)
                    .padding(.top, 0)
            }
            .fixedSize(horizontal: false, vertical: true)

            VStack(spacing: 0) {
                Text("🇰🇷 서울: \(timeSeoul)")
                    .foregroundColor(Color(hex: "#76D4EB") ?? .blue)
                    .font(.system(size: 20, weight: .bold))
                
                Text("🇦🇺 Sydney: \(timeSydney)")
                    .foregroundColor(Color(hex: "#58CD3E") ?? .green)
                    .font(.system(size: 20, weight: .bold))
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .background(Color.black)
        .onAppear {
            startTimer()
        }
    }
    
    // Logic for angles
    private var hourAngle: Double {
        let components = Calendar.current.dateComponents([.hour, .minute], from: currentTime)
        let hour = Double(components.hour ?? 0)
        let minute = Double(components.minute ?? 0)
        return (hour * 30) + (minute * 0.5)
    }
    
    private var minuteAngle: Double {
        let minute = Double(Calendar.current.component(.minute, from: currentTime))
        return minute * 6
    }
    
    private var secondAngle: Double {
        let second = Double(Calendar.current.component(.second, from: currentTime))
        return second * 6
    }
    
    private func startTimer() {
        Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            currentTime = Date()
            updateWorldTimes()
        }
    }
    
    private func updateWorldTimes() {
        let formatter = DateFormatter()
        formatter.dateFormat = "MM-dd HH:mm"
        
        formatter.timeZone = timeZoneSeoul
        timeSeoul = formatter.string(from: currentTime)
        
        formatter.timeZone = timeZoneSydney
        timeSydney = formatter.string(from: currentTime)
    }
    
    private func formYear(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy"
        return formatter.string(from: date)
    }
    
    private func formDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "MM-dd"
        return formatter.string(from: date)
    }
    
    private func formDoW(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "EEE"
        let hanDoW = formatter.string(from: date)
        formatter.locale = Locale(identifier: "en_US")
        formatter.dateFormat = "EE"
        let engDoW = formatter.string(from: date)
        return engDoW + " (" + hanDoW + ")"
    }
}

struct ClockHand: Shape {
    var length: CGFloat
    var angle: Double
    
    func path(in rect: CGRect) -> Path {
        var path = Path()
        let rad = angle * .pi / 180.0
        let x = cos(rad) * length
        let y = sin(rad) * length
        path.move(to: CGPoint(x: rect.midX, y: rect.midY))
        path.addLine(to: CGPoint(x: rect.midX + x, y: rect.midY + y))
        return path
    }
}

extension Color {
    init?(hex: String) {
        var hexSanitized = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        hexSanitized = hexSanitized.replacingOccurrences(of: "#", with: "")
        
        var rgb: UInt64 = 0
        // Using the correct scanHexInt64 we discussed!
        Scanner(string: hexSanitized).scanHexInt64(&rgb)
        
        let red = Double((rgb >> 16) & 0xFF) / 255.0
        let green = Double((rgb >> 8) & 0xFF) / 255.0
        let blue = Double(rgb & 0xFF) / 255.0
        
        self.init(red: red, green: green, blue: blue)
    }
}

