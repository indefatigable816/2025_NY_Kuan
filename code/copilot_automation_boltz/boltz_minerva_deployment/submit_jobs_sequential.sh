#!/bin/bash

# Sequential Job Submission Script for HER2 Boltz Predictions on Minerva
# This script submits all boltz prediction jobs one at a time
# Each job completes before the next one is submitted to avoid GPU overload

set -e  # Exit on any error

WKDIR="/sc/arion/work/cheny69/1216"
LOG_DIR="${WKDIR}/submission_logs"
SUBMISSION_START=$(date '+%Y-%m-%d_%H-%M-%S')

# Create log directory
mkdir -p ${LOG_DIR}

echo "=========================================="
echo "HER2 Boltz Sequential Job Submission"
echo "=========================================="
echo "Working Directory: ${WKDIR}"
echo "Log Directory: ${LOG_DIR}"
echo "Submission Start: ${SUBMISSION_START}"
echo ""

# Array of all jobs in submission order
declare -a JOBS=(
    # Monomer/ECD predictions
    "d16"
    "WT_ECD"
    "S310F"
    
    # Monomer/ICD predictions
    "WT_ICD"
    "K753E"
    "L755S"
    
    # Multimer/dimer predictions
    "WT_dimer"
    "d16_dimer"
    
    # Multimer/drug-binding predictions (trastuzumab)
    "WT_trastuzumab"
    "d16_trastuzumab"
    
    # Multimer/drug-binding predictions (pertuzumab)
    "WT_pertuzumab"
    "S310F_pertuzumab"
    
    # Multimer/drug-binding predictions (lapatinib)
    "WT_lapatinib"
    "K753E_lapatinib"
    "L755S_lapatinib"
)

TOTAL_JOBS=${#JOBS[@]}
echo "Total jobs to submit: ${TOTAL_JOBS}"
echo ""

# Change to working directory
cd ${WKDIR}

# Track results
SUCCEEDED=0
FAILED=0
SUBMISSION_LOG="${LOG_DIR}/submissions_${SUBMISSION_START}.log"

echo "Submission Log: ${SUBMISSION_LOG}" > ${SUBMISSION_LOG}
echo "Started: $(date)" >> ${SUBMISSION_LOG}
echo "" >> ${SUBMISSION_LOG}

# Submit each job sequentially
for ((i=0; i<${TOTAL_JOBS}; i++)); do
    JOB=${JOBS[$i]}
    JOB_NUM=$((i+1))
    
    echo "[${JOB_NUM}/${TOTAL_JOBS}] Submitting ${JOB}..."
    
    if [ -f "${JOB}.lsf" ] && [ -f "${JOB}.yaml" ]; then
        # Submit the job
        JOB_ID=$(bsub < ${JOB}.lsf 2>&1 | grep -oP 'Job <\K[0-9]+')
        
        if [ ! -z "$JOB_ID" ]; then
            echo "  ✓ Job ID: ${JOB_ID}"
            echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: Job ID ${JOB_ID} submitted at $(date)" >> ${SUBMISSION_LOG}
            SUCCEEDED=$((SUCCEEDED+1))
            
            # Wait a bit before submitting next job (to avoid queue overload)
            echo "  Waiting 5 seconds before next submission..."
            sleep 5
        else
            echo "  ✗ Failed to submit ${JOB}"
            echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: FAILED at $(date)" >> ${SUBMISSION_LOG}
            FAILED=$((FAILED+1))
        fi
    else
        echo "  ✗ Missing files: ${JOB}.lsf or ${JOB}.yaml"
        echo "[${JOB_NUM}/${TOTAL_JOBS}] ${JOB}: MISSING FILES at $(date)" >> ${SUBMISSION_LOG}
        FAILED=$((FAILED+1))
    fi
done

# Print summary
echo ""
echo "=========================================="
echo "Submission Summary"
echo "=========================================="
echo "Total jobs submitted: ${SUCCEEDED}"
echo "Total jobs failed: ${FAILED}"
echo "Submission End: $(date)"
echo ""
echo "Submission Log: ${SUBMISSION_LOG}"
echo ""
echo "To monitor job status, use:"
echo "  bjobs                           # Check all your jobs"
echo "  bjobs -a                        # Include finished jobs"
echo "  bhist                           # Show job history"
echo "  bjobs -l <JOB_ID>               # Detailed info on specific job"
echo ""
echo "To check output files:"
echo "  ls -la ${WKDIR}/results/"
echo ""

# Append summary to log
echo "" >> ${SUBMISSION_LOG}
echo "Completed: $(date)" >> ${SUBMISSION_LOG}
echo "Succeeded: ${SUCCEEDED}" >> ${SUBMISSION_LOG}
echo "Failed: ${FAILED}" >> ${SUBMISSION_LOG}

exit 0
