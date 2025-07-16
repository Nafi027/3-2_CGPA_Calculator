import streamlit as st
import pandas as pd
from datetime import datetime
import os
import hashlib

# Page configuration
st.set_page_config(
    page_title="CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# Constants
COURSES = {
    "Basic Communication Engineering": 3.00,
    "Basic Communication Engineering Lab": 1.50,
    "Microprocessor & Interfacing": 3.00,
    "Microprocessor & Interfacing Lab": 1.50,
    "Control System I": 3.00,
    "Control System I Lab": 1.50,
    "Power System II": 3.00,
    "Power Electronics": 3.00,
    "Power Electronics Lab": 1.50
}

# Admin credentials
ADMIN_ID = "2020338027"
ADMIN_PASSWORD = "2020338027"

# File paths
DATA_FILE = "student_cgpa_data.csv"
BACKUP_FILE = "student_cgpa_backup.csv"

# Initialize session state
if 'registered' not in st.session_state:
    st.session_state.registered = False
if 'student_data' not in st.session_state:
    st.session_state.student_data = {}
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_to_csv(data):
    """Save student data to CSV file"""
    try:
        # Check if file exists
        if os.path.exists(DATA_FILE):
            df_existing = pd.read_csv(DATA_FILE)
            df_new = pd.DataFrame([data])
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = pd.DataFrame([data])
        
        # Save to file
        df_combined.to_csv(DATA_FILE, index=False)
        
        # Create backup
        df_combined.to_csv(BACKUP_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving data: {str(e)}")
        return False

def load_csv_data():
    """Load student data from CSV file"""
    try:
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
    }
    .cgpa-display {
        font-size: 3rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .admin-header {
        background-color: #1f1f1f;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation
col1, col2, col3 = st.columns([1, 3, 1])
with col3:
    if st.session_state.page == 'main':
        if st.button("🔐 Admin Login"):
            st.session_state.page = 'admin'
            st.rerun()
    elif st.session_state.page == 'admin' and not st.session_state.admin_logged_in:
        if st.button("🏠 Back to Main"):
            st.session_state.page = 'main'
            st.rerun()
    elif st.session_state.admin_logged_in:
        if st.button("🚪 Logout Admin"):
            st.session_state.admin_logged_in = False
            st.session_state.page = 'main'
            st.rerun()

# Main Application
if st.session_state.page == 'main':
    # Header
    st.title("🎓 CGPA Calculator")
    st.markdown("---")

    # Registration Section
    if not st.session_state.registered:
        st.header("Student Registration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            reg_number = st.text_input("Registration Number", placeholder="Enter your registration number")
        
        with col2:
            student_name = st.text_input("Student Name", placeholder="Enter your full name")
        
        if st.button("Register", type="primary"):
            if reg_number and student_name:
                st.session_state.registered = True
                st.session_state.student_data = {
                    "reg_number": reg_number,
                    "name": student_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.success(f"Welcome, {student_name}! You can now calculate your CGPA.")
                st.rerun()
            else:
                st.error("Please fill in all fields!")

    # CGPA Calculation Section
    else:
        # Display student info
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.info(f"**Registration Number:** {st.session_state.student_data['reg_number']}")
        
        with col2:
            st.info(f"**Name:** {st.session_state.student_data['name']}")
        
        with col3:
            if st.button("Logout"):
                st.session_state.registered = False
                st.session_state.student_data = {}
                st.rerun()
        
        st.markdown("---")
        
        # Course Grade Input Section
        st.header("Enter Your Course GPAs")
        
        # Information box
        st.markdown("""
        <div class="warning-box">
        <b>📌 Instructions:</b><br>
        • Enter GPA (0.00 - 4.00) for completed courses<br>
        • Leave blank for dropped/not taken courses<br>
        • Dropped courses will not affect your CGPA calculation
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for better layout
        course_gpas = {}
        
        # Display courses in a grid layout
        for i, (course, credit) in enumerate(COURSES.items()):
            col1, col2, col3 = st.columns([3, 1, 2])
            
            with col1:
                st.write(f"**{course}**")
            
            with col2:
                st.write(f"Credits: {credit}")
            
            with col3:
                gpa = st.number_input(
                    "GPA",
                    min_value=0.00,
                    max_value=4.00,
                    value=None,
                    step=0.01,
                    format="%.2f",
                    key=f"gpa_{i}",
                    label_visibility="collapsed",
                    placeholder="Enter GPA"
                )
                if gpa is not None:
                    course_gpas[course] = gpa
        
        st.markdown("---")
        
        # Calculate CGPA Button
        if st.button("Calculate CGPA", type="primary"):
            # Calculate CGPA
            total_weighted_gpa = 0
            total_credits = 0
            courses_included = []
            courses_excluded = []
            
            # Prepare data for saving
            save_data = {
                "Registration_Number": st.session_state.student_data['reg_number'],
                "Name": st.session_state.student_data['name'],
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add course GPAs to save data
            for course, credit in COURSES.items():
                course_column = course.replace(" ", "_").replace("&", "and")
                if course in course_gpas:
                    gpa = course_gpas[course]
                    save_data[f"{course_column}_GPA"] = gpa
                    save_data[f"{course_column}_Credit"] = credit
                    total_weighted_gpa += gpa * credit
                    total_credits += credit
                    courses_included.append({
                        "Course": course,
                        "Credit": credit,
                        "GPA": gpa,
                        "Weighted": gpa * credit
                    })
                else:
                    save_data[f"{course_column}_GPA"] = "Dropped"
                    save_data[f"{course_column}_Credit"] = 0
                    courses_excluded.append(course)
            
            # Display Results
            st.header("📊 Results")
            
            if total_credits > 0:
                cgpa = total_weighted_gpa / total_credits
                save_data["CGPA"] = round(cgpa, 2)
                save_data["Total_Credits"] = total_credits
                save_data["Courses_Taken"] = len(courses_included)
                save_data["Courses_Dropped"] = len(courses_excluded)
                
                # Save to CSV
                if save_to_csv(save_data):
                    st.success("✅ Your data has been saved successfully!")
                
                # Display CGPA
                st.markdown(f"""
                    <div class="result-box">
                        <h2>Your Calculated CGPA</h2>
                        <div class="cgpa-display">{cgpa:.2f}</div>
                        <p>Out of 4.00</p>
                        <p style="color: #666; margin-top: 1rem;">
                            Formula: Σ(GPA × Credit) / Σ(Credits) = {total_weighted_gpa:.2f} / {total_credits:.1f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Display summary metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Credits Counted", f"{total_credits:.1f}")
                
                with col2:
                    st.metric("Courses Included", len(courses_included))
                
                with col3:
                    st.metric("Courses Excluded", len(courses_excluded))
                
                # Show detailed breakdown
                with st.expander("📋 View Detailed Breakdown"):
                    if courses_included:
                        st.subheader("Courses Included in CGPA:")
                        df_included = pd.DataFrame(courses_included)
                        df_included = df_included.round(2)
                        st.dataframe(df_included, use_container_width=True)
                    
                    if courses_excluded:
                        st.subheader("Courses Excluded (Dropped/Not Taken):")
                        for course in courses_excluded:
                            st.write(f"- {course}")
            else:
                st.error("No course data provided! Please enter GPA for at least one course.")

# Admin Panel
elif st.session_state.page == 'admin':
    st.markdown('<div class="admin-header"><h1>🔐 Admin Panel</h1></div>', unsafe_allow_html=True)
    
    if not st.session_state.admin_logged_in:
        # Admin Login
        st.header("Admin Login")
        
        col1, col2 = st.columns(2)
        with col1:
            admin_id = st.text_input("Admin ID", type="password")
        with col2:
            admin_password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            if admin_id == ADMIN_ID and admin_password == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
    
    else:
        # Admin Dashboard
        st.header("📊 Student CGPA Database")
        
        # Load data
        df = load_csv_data()
        
        if not df.empty:
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Students", len(df))
            with col2:
                avg_cgpa = df['CGPA'].mean() if 'CGPA' in df.columns else 0
                st.metric("Average CGPA", f"{avg_cgpa:.2f}")
            with col3:
                if 'CGPA' in df.columns:
                    highest_cgpa = df['CGPA'].max()
                    st.metric("Highest CGPA", f"{highest_cgpa:.2f}")
            with col4:
                if 'CGPA' in df.columns:
                    lowest_cgpa = df['CGPA'].min()
                    st.metric("Lowest CGPA", f"{lowest_cgpa:.2f}")
            
            st.markdown("---")
            
            # Data filters
            st.subheader("🔍 Filter Options")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_reg = st.text_input("Search by Registration Number")
            with col2:
                search_name = st.text_input("Search by Name")
            with col3:
                if 'CGPA' in df.columns:
                    cgpa_range = st.slider(
                        "CGPA Range",
                        min_value=0.0,
                        max_value=4.0,
                        value=(0.0, 4.0),
                        step=0.1
                    )
            
            # Apply filters
            filtered_df = df.copy()
            if search_reg:
                filtered_df = filtered_df[filtered_df['Registration_Number'].astype(str).str.contains(search_reg)]
            if search_name:
                filtered_df = filtered_df[filtered_df['Name'].str.contains(search_name, case=False)]
            if 'CGPA' in df.columns:
                filtered_df = filtered_df[(filtered_df['CGPA'] >= cgpa_range[0]) & (filtered_df['CGPA'] <= cgpa_range[1])]
            
            # Display data
            st.subheader(f"📋 Student Records ({len(filtered_df)} records)")
            
                        # Display options
            col1, col2 = st.columns([3, 1])
            with col1:
                display_columns = st.multiselect(
                    "Select columns to display",
                    options=filtered_df.columns.tolist(),
                    default=['Registration_Number', 'Name', 'CGPA', 'Total_Credits', 'Timestamp'] if all(col in filtered_df.columns for col in ['Registration_Number', 'Name', 'CGPA', 'Total_Credits', 'Timestamp']) else filtered_df.columns.tolist()[:5]
                )
            with col2:
                show_all_columns = st.checkbox("Show all columns")
            
            if show_all_columns:
                st.dataframe(filtered_df, use_container_width=True, height=400)
            else:
                if display_columns:
                    st.dataframe(filtered_df[display_columns], use_container_width=True, height=400)
                else:
                    st.warning("Please select at least one column to display")
            
            # Export options
            st.markdown("---")
            st.subheader("📥 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download filtered data as CSV
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download Filtered Data (CSV)",
                    data=csv,
                    file_name=f"cgpa_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Download full data as CSV
                full_csv = df.to_csv(index=False)
                st.download_button(
                    label="📊 Download All Data (CSV)",
                    data=full_csv,
                    file_name=f"cgpa_data_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col3:
                # Download as Excel
                try:
                    import io
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        filtered_df.to_excel(writer, sheet_name='CGPA_Data', index=False)
                    
                    st.download_button(
                        label="📑 Download as Excel",
                        data=buffer.getvalue(),
                        file_name=f"cgpa_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except ImportError:
                    st.error("Excel export requires openpyxl. Install it using: pip install openpyxl")
            
            # Analytics Section
            st.markdown("---")
            st.subheader("📈 Analytics")
            
            tab1, tab2, tab3 = st.tabs(["CGPA Distribution", "Course Analysis", "Time Analysis"])
            
            with tab1:
                if 'CGPA' in filtered_df.columns and len(filtered_df) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # CGPA Distribution
                        st.subheader("CGPA Distribution")
                        cgpa_bins = [0, 2.0, 2.5, 3.0, 3.5, 3.75, 4.0]
                        cgpa_labels = ['0-2.0', '2.0-2.5', '2.5-3.0', '3.0-3.5', '3.5-3.75', '3.75-4.0']
                        filtered_df['CGPA_Range'] = pd.cut(filtered_df['CGPA'], bins=cgpa_bins, labels=cgpa_labels, include_lowest=True)
                        cgpa_dist = filtered_df['CGPA_Range'].value_counts().sort_index()
                        st.bar_chart(cgpa_dist)
                    
                    with col2:
                        # Performance Categories
                        st.subheader("Performance Categories")
                        performance_data = {
                            'Outstanding (3.75-4.0)': len(filtered_df[filtered_df['CGPA'] >= 3.75]),
                            'Excellent (3.5-3.75)': len(filtered_df[(filtered_df['CGPA'] >= 3.5) & (filtered_df['CGPA'] < 3.75)]),
                            'Very Good (3.0-3.5)': len(filtered_df[(filtered_df['CGPA'] >= 3.0) & (filtered_df['CGPA'] < 3.5)]),
                            'Good (2.5-3.0)': len(filtered_df[(filtered_df['CGPA'] >= 2.5) & (filtered_df['CGPA'] < 3.0)]),
                            'Satisfactory (2.0-2.5)': len(filtered_df[(filtered_df['CGPA'] >= 2.0) & (filtered_df['CGPA'] < 2.5)]),
                            'Poor (<2.0)': len(filtered_df[filtered_df['CGPA'] < 2.0])
                        }
                        st.bar_chart(pd.Series(performance_data))
            
            with tab2:
                st.subheader("Course-wise Analysis")
                # Extract course columns
                course_columns = [col for col in filtered_df.columns if '_GPA' in col and not col.startswith('CGPA')]
                
                if course_columns:
                    # Calculate average GPA per course
                    course_stats = []
                    for col in course_columns:
                        course_name = col.replace('_GPA', '').replace('_', ' ').replace('and', '&')
                        # Filter only numeric values (not "Dropped")
                        numeric_mask = filtered_df[col] != "Dropped"
                        numeric_data = filtered_df[numeric_mask][col]
                        
                        if len(numeric_data) > 0:
                            try:
                                numeric_gpas = pd.to_numeric(numeric_data, errors='coerce')
                                valid_gpas = numeric_gpas.dropna()
                                if len(valid_gpas) > 0:
                                    course_stats.append({
                                        'Course': course_name,
                                        'Average GPA': valid_gpas.mean(),
                                        'Students Enrolled': len(valid_gpas),
                                        'Students Dropped': len(filtered_df) - len(valid_gpas)
                                    })
                            except:
                                pass
                    
                    if course_stats:
                        stats_df = pd.DataFrame(course_stats)
                        st.dataframe(stats_df.round(2), use_container_width=True, hide_index=True)
                        
                        # Bar chart of average GPAs
                        st.subheader("Average GPA by Course")
                        chart_data = stats_df.set_index('Course')['Average GPA']
                        st.bar_chart(chart_data)
            
            with tab3:
                if 'Timestamp' in filtered_df.columns:
                    st.subheader("Submissions Over Time")
                    try:
                        # Convert timestamp to datetime
                        filtered_df['Date'] = pd.to_datetime(filtered_df['Timestamp']).dt.date
                        daily_counts = filtered_df.groupby('Date').size()
                        if len(daily_counts) > 0:
                            st.line_chart(daily_counts)
                        
                        # Monthly distribution
                        filtered_df['Month'] = pd.to_datetime(filtered_df['Timestamp']).dt.to_period('M')
                        monthly_counts = filtered_df.groupby('Month').size()
                        if len(monthly_counts) > 0:
                            st.subheader("Monthly Submissions")
                            st.bar_chart(monthly_counts)
                    except:
                        st.info("Unable to process time data")
            
            # Data Management
            st.markdown("---")
            st.subheader("🛠️ Data Management")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Refresh Data", type="primary"):
                    st.rerun()
            
            with col2:
                if st.button("📊 Generate Report"):
                    # Create a comprehensive report
                    report = f"""
CGPA DATABASE REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS:
- Total Students: {len(df)}
- Average CGPA: {df['CGPA'].mean():.2f}
- Highest CGPA: {df['CGPA'].max():.2f}
- Lowest CGPA: {df['CGPA'].min():.2f}
- Standard Deviation: {df['CGPA'].std():.2f}

PERFORMANCE DISTRIBUTION:
- Outstanding (3.75-4.0): {len(df[df['CGPA'] >= 3.75])} students
- Excellent (3.5-3.75): {len(df[(df['CGPA'] >= 3.5) & (df['CGPA'] < 3.75)])} students
- Very Good (3.0-3.5): {len(df[(df['CGPA'] >= 3.0) & (df['CGPA'] < 3.5)])} students
- Good (2.5-3.0): {len(df[(df['CGPA'] >= 2.5) & (df['CGPA'] < 3.0)])} students
- Satisfactory (2.0-2.5): {len(df[(df['CGPA'] >= 2.0) & (df['CGPA'] < 2.5)])} students
- Poor (<2.0): {len(df[df['CGPA'] < 2.0])} students
                    """
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"cgpa_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            with col3:
                # Delete specific record
                if st.checkbox("Enable Delete Mode"):
                    st.warning("⚠️ Delete Mode Active")
                    delete_reg = st.selectbox(
                        "Select student to delete",
                        options=df['Registration_Number'].tolist(),
                        format_func=lambda x: f"{x} - {df[df['Registration_Number']==x]['Name'].values[0]}"
                    )
                    if st.button("🗑️ Delete Selected", type="secondary"):
                        df_updated = df[df['Registration_Number'] != delete_reg]
                        df_updated.to_csv(DATA_FILE, index=False)
                        st.success(f"Deleted record for {delete_reg}")
                        st.rerun()
            
            # Individual Student View
            st.markdown("---")
            st.subheader("👤 Individual Student View")
            
            if not filtered_df.empty:
                selected_reg = st.selectbox(
                    "Select a student to view details",
                    options=filtered_df['Registration_Number'].tolist(),
                    format_func=lambda x: f"{x} - {filtered_df[filtered_df['Registration_Number']==x]['Name'].values[0]}"
                )
                
                if selected_reg:
                    student_data = filtered_df[filtered_df['Registration_Number'] == selected_reg].iloc[0]
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("### Student Information")
                        st.write(f"**Name:** {student_data['Name']}")
                        st.write(f"**Registration:** {student_data['Registration_Number']}")
                        st.write(f"**CGPA:** {student_data.get('CGPA', 'N/A')}")
                        st.write(f"**Total Credits:** {student_data.get('Total_Credits', 'N/A')}")
                        st.write(f"**Courses Taken:** {student_data.get('Courses_Taken', 'N/A')}")
                        st.write(f"**Courses Dropped:** {student_data.get('Courses_Dropped', 'N/A')}")
                        st.write(f"**Submission Time:** {student_data.get('Timestamp', 'N/A')}")
                    
                    with col2:
                        st.markdown("### Course Details")
                        course_data = []
                        for course in COURSES.keys():
                            course_col = course.replace(" ", "_").replace("&", "and")
                            gpa_col = f"{course_col}_GPA"
                            if gpa_col in student_data:
                                gpa_value = student_data[gpa_col]
                                if gpa_value != "Dropped":
                                    course_data.append({
                                        "Course": course,
                                        "GPA": gpa_value,
                                        "Credit": COURSES[course],
                                        "Weighted": float(gpa_value) * COURSES[course]
                                    })
                        
                        if course_data:
                            course_df = pd.DataFrame(course_data)
                            st.dataframe(course_df, use_container_width=True, hide_index=True)
                            
                            # Show calculation
                            total_weighted = sum(c["Weighted"] for c in course_data)
                            total_credits = sum(c["Credit"] for c in course_data)
                            st.info(f"**CGPA Calculation:** {total_weighted:.2f} ÷ {total_credits:.1f} = {student_data.get('CGPA', 'N/A')}")
        
        else:
            st.info("No student data available yet.")
            
            # Option to upload existing data
            st.markdown("---")
            st.subheader("📤 Import Data")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    uploaded_df = pd.read_csv(uploaded_file)
                    st.write("Preview of uploaded data:")
                    st.dataframe(uploaded_df.head(), use_container_width=True)
                    
                    if st.button("Import Data", type="primary"):
                        uploaded_df.to_csv(DATA_FILE, index=False)
                        st.success("Data imported successfully!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Error importing data: {str(e)}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>3/2 CGPA Calculator © Md. Nafiul Hasnat | Built with Streamlit</p>
        <p style='font-size: 0.8rem;'>Formula: CGPA = Σ(GPA × Credit) / Σ(Credits of courses with GPA)</p>
    </div>
    """,
    unsafe_allow_html=True
) 