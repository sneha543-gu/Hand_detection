import streamlit as st
import cv2
from cvzone.HandTrackingModule import HandDetector
import os
import boto3
import webbrowser

# Streamlit Page Configuration
st.set_page_config(page_title="Gesture Control", page_icon="🖐️", layout="wide")

# Page Header
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: 700;
            color: white;
            background-color: #4A90E2;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .footer {
            color: gray;
            font-size: 14px;
            margin-top: 30px;
        }
    </style>
    <div class='main-title'>🖐️ Gesture-Controlled Action Dashboard</div>
""", unsafe_allow_html=True)

# Layout Columns
left_col, right_col = st.columns([2, 1])

with left_col:
    st.markdown("### 📸 Webcam Capture")

    if st.button("Start Camera & Detect Gesture"):
        cap = cv2.VideoCapture(0)
        st.info("Press 's' to capture, 'q' to quit (in webcam window)")

        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Webcam not accessible.")
                break

            cv2.imshow("Webcam - Press 's' to Save, 'q' to Quit", frame)
            key = cv2.waitKey(1)

            if key == ord('s'):
                cv2.imwrite("captured.jpg", frame)
                cap.release()
                cv2.destroyAllWindows()

                # Hand Detection
                detector = HandDetector(detectionCon=0.7)
                hands, _ = detector.findHands(frame, draw=True)

                if hands:
                    fingers = detector.fingersUp(hands[0])
                else:
                    fingers = None

                # Display Image with Hand Landmark
                st.image(frame, caption="📷 Captured Gesture")

                # Display finger count directly below image
                if fingers:
                    st.markdown(f"<h4 style='text-align:center;color:green;'>🖐️ Fingers Detected: {fingers}</h4>", unsafe_allow_html=True)
                else:
                    st.markdown("<h4 style='text-align:center;color:red;'>🙅 No hand detected.</h4>", unsafe_allow_html=True)

                # Trigger Actions
                if fingers:
                    if fingers == [0, 0, 0, 0, 0]:  # 0 Fingers
                        os.system('notepad')
                        st.success("📝 Opened Notepad")

                    elif fingers == [1, 0, 0, 0, 0]:  # Thumb Only
                        os.system('start chrome')
                        st.success("🌐 Opened Chrome")

                    elif fingers == [0, 1, 0, 0, 0]:  # Index Only
                        os.system('start msedge')
                        st.success("🌐 Opened Edge")

                    elif fingers == [0, 1, 1, 0, 0]:  # Index + Middle
                        st.info("🚀 Launching EC2 Instance...")
                        try:
                            ec2 = boto3.resource('ec2', region_name="ap-south-1")
                            ec2.create_instances(
                                InstanceType='t3.micro',
                                ImageId='ami-0d0ad8bb301edb745',
                                MinCount=1,
                                MaxCount=1
                            )
                            st.success("✅ EC2 Instance Started")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

                    elif fingers == [0, 1, 1, 1, 0]:  # Index + Middle + Ring
                        st.info("⛔ Stopping EC2 Instance...")
                        try:
                            ec2 = boto3.client('ec2', region_name="ap-south-1")
                            instance_id = 'i-0c9222ddc82c51785'
                            ec2.stop_instances(InstanceIds=[instance_id])
                            st.success(f"✅ Instance {instance_id} Stopped")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

                    elif fingers == [0, 1, 1, 1, 1]:  # All Fingers
                        webbrowser.open("https://www.youtube.com")
                        st.success("▶️ Opened YouTube")

                    elif fingers == [1, 1, 1, 1, 1]:  # Middle + Ring + Pinky
                        os.system("explorer")
                        st.success("📁 Opened File Explorer")

                    elif fingers == [0, 1, 0, 1, 1]:  # Custom Combo: Index + Ring + Pinky
                        webbrowser.open("https://www.google.com")
                        st.success("🔍 Opened Google")

                    else:
                        st.warning("🤷 Unrecognized Gesture.")
                break

            elif key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                st.warning("❌ Quit without capturing.")
                break

with right_col:
    st.markdown("### ✋ Gesture Guide")
    st.markdown("""
    <div style="background-color:#656475;padding:12px;border-radius:10px;line-height:1.8">
    🟢 0 Fingers: <b>Open Notepad</b><br>
    🟢 1 Finger (Thumb): <b>Open Chrome</b><br>
    🟢 1 Finger (Index): <b>Open Edge</b><br>
    🟢 2 Fingers (Index + Middle): <b>Start EC2 Instance</b><br>
    🟢 3 Fingers (Index + Middle + Ring): <b>Stop EC2 Instance</b><br>
    🟢 5 Fingers: <b>Open YouTube</b><br>
    🟢 3 Fingers (Middle + Ring + Pinky): <b>Open File Explorer</b><br>
    🟢 Custom Combo (Index + Ring + Pinky): <b>Open Google</b><br>
    </div>
    """, unsafe_allow_html=True)
