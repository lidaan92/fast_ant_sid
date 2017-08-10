    ! _AIS SOLID ICE DISCHARGE CONTRIBUTION__________________________________________________________
    
    SLR_AIS_SID_STARTYEAR_RUN = SLR_AIS_SID_STARTYEAR - 1
    
    ! CHOOSE SLR AIS SID METHOD 'DECONTO' OR 'LEVERMANN'
    IF (SLR_AIS_SID_PARAMETERISATION == 'DECONTO') THEN
    
        ! START WITH SLR_AIS_SID_STARTYEAR
        IF ((STARTYEAR+CURRENT_YEAR_IDX) > SLR_AIS_SID_STARTYEAR_RUN) THEN
            
            ! EXIT AIS SID ROUTINE IF CURRENT DAT_SURFACE_ANNUALMEANTEMP EQUALS ZERO
            IF (DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) == 0.) THEN
                
                SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) = SLR_AIS_SID_CONTRIBUTION(CURRENT_YEAR_IDX)
            
            ELSE            
                ! DEFINE START DISCHARGEVOLUMES
                IF (SLR_AIS_SID_STARTYEAR == STARTYEAR) THEN 
                    SLR_AIS_SID_DSCHRGVOL(SLR_AIS_SID_STARTYEAR_RUN - STARTYEAR + 2) = &
                        SLR_AIS_SID_TOTALVOL           
                ELSE        
                    SLR_AIS_SID_DSCHRGVOL(SLR_AIS_SID_STARTYEAR_RUN - STARTYEAR + 1) = &
                        SLR_AIS_SID_TOTALVOL
                END IF            
                 
                ! CHECK IF FAST PROCESS HAS TO BE TRIGGERED 
                IF (DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) < &
                    SLR_AIS_SID_THRESHOLDTEMP) THEN    
                    AIS_SID_DISCHARGE = SLR_AIS_SID_DSCHRG_SENS * &
                        SLR_AIS_SID_DSCHRGVOL(CURRENT_YEAR_IDX) * &
                        SIGN((DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) - &
                        SLR_AIS_SID_ZEROTEMP)**SLR_AIS_SID_TEMPSENS_EXPONENT,&
                        (DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) - &
                        SLR_AIS_SID_ZEROTEMP))
                ELSE
                    AIS_SID_DISCHARGE = SLR_AIS_SID_DSCHRG_SENS * &
                        SLR_AIS_SID_DSCHRGVOL(CURRENT_YEAR_IDX) * &
                        SIGN((DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) - &
                        SLR_AIS_SID_ZEROTEMP)**SLR_AIS_SID_TEMPSENS_EXPONENT,&
                        (DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) - &
                        SLR_AIS_SID_ZEROTEMP)) + &
                        SLR_AIS_SID_FASTRATE
                END IF
                
                AIS_SID_DISCHARGE = &
                   MIN(AIS_SID_DISCHARGE,SLR_AIS_SID_DSCHRGVOL(CURRENT_YEAR_IDX)) 
                    
                ! DETERMINE REMAINING DISCHARGEVOL FOR EACH CASE AND
                ! DO NOT DEPLETE DISCHARGEVOLUMES PRIOR TO CALIBRATION START YEAR 1950
                IF ((STARTYEAR+CURRENT_YEAR_IDX-1) < 1950) THEN
                    SLR_AIS_SID_DSCHRGVOL(NEXT_YEAR_IDX) = SLR_AIS_SID_TOTALVOL                    
                    SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) = &
                       SLR_AIS_SID_CONTRIBUTION(CURRENT_YEAR_IDX) + AIS_SID_DISCHARGE
                ELSE    
                    SLR_AIS_SID_DSCHRGVOL(NEXT_YEAR_IDX) = &
                        SLR_AIS_SID_DSCHRGVOL(CURRENT_YEAR_IDX) - AIS_SID_DISCHARGE                        
                    SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) = SLR_AIS_SID_TOTALVOL - &
                        SLR_AIS_SID_DSCHRGVOL(NEXT_YEAR_IDX) + &
                        SLR_AIS_SID_CONTRIBUTION(1950-SLR_AIS_SID_STARTYEAR+1)                    
                END IF
                        
                ! DETERMINE AIS SID SLR, SCALE WITH FACTOR IF NEED BE      
                SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) = &
                    SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) * SLR_AIS_SID_SCALING

            END IF   
            
            ! MAKE SURE THAT CONTRIBUTION IS NaN WHENEVER TEMP FORCING IS NaN
            IF (ISNAN(DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX))) THEN
                NaN = 0.
                NaN = NaN/NaN
                SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX) = NaN
            END IF
                            
        END IF
        
    ELSE
        
        IF ((STARTYEAR+CURRENT_YEAR_IDX-1) > SLR_AIS_SID_STARTYEAR_RUN) THEN
            
            IF (SLR_AIS_SID_ICEMODEL == 'PISM') THEN
                SLR_AIS_SID_R_AMUNDSEN = SLR_AIS_SID_R_AMUNDSEN_PISM
                SLR_AIS_SID_R_EASTANTARCTICA = SLR_AIS_SID_R_EASTANTARCTICA_PISM
                SLR_AIS_SID_R_ROSS = SLR_AIS_SID_R_ROSS_PISM
                SLR_AIS_SID_R_WEDDELL = SLR_AIS_SID_R_WEDDELL_PISM
            ELSEIF (SLR_AIS_SID_ICEMODEL == 'SICOPOLIS') THEN
                SLR_AIS_SID_R_AMUNDSEN = SLR_AIS_SID_R_AMUNDSEN_SICOPOLIS
                SLR_AIS_SID_R_EASTANTARCTICA = SLR_AIS_SID_R_EASTANTARCTICA_SICOPOLIS
                SLR_AIS_SID_R_ROSS = SLR_AIS_SID_R_ROSS_SICOPOLIS
                SLR_AIS_SID_R_WEDDELL = SLR_AIS_SID_R_WEDDELL_SICOPOLIS
            ELSE
                SLR_AIS_SID_R_AMUNDSEN = SLR_AIS_SID_R_AMUNDSEN_PENNSTATE3D
                SLR_AIS_SID_R_EASTANTARCTICA = SLR_AIS_SID_R_EASTANTARCTICA_PENNSTATE3D
                SLR_AIS_SID_R_ROSS = SLR_AIS_SID_R_ROSS_PENNSTATE3D
                SLR_AIS_SID_R_WEDDELL = SLR_AIS_SID_R_WEDDELL_PENNSTATE3D
            END IF
            
            ! DEFINE AIS SID IDX TO REPLACE CURRENT_YEAR_IDX FOR R, START COUNT WITH SLR_AIS_SID_STARTYEAR
            AIS_SID_IDX = CURRENT_YEAR_IDX - (SLR_AIS_SID_STARTYEAR - STARTYEAR)
            
            ! PICK RANDOM NUMBER BETWEEN MIN/MAX EMPIRICAL MELT SENSITIVITIES
            IF (SLR_AIS_SID_PRESCRIBE_BASALMELT == 1) THEN
                SLR_AIS_SID_BASALMELT_RANDOM = SLR_AIS_SID_BASALMELT
            ELSE
                SLR_AIS_SID_BASALMELT_RANDOM = SLR_AIS_SID_BASALMELT_SENS(1) + &
                    INT((SLR_AIS_SID_BASALMELT_SENS(2)-SLR_AIS_SID_BASALMELT_SENS(1)) * RAND())
            END IF
            
            DO R = 1,SIZE(SLR_AIS_SID_REGION)
                
                ! SELECT REGION SPECIFIC PARAMETERS AND CUT THE R-ARRAYS TO NYEARS STARTING FROM
                ! LAST ELEMENT BECAUSE FLIPPED
                IF (R == 1) THEN
                    SLR_AIS_SID_DT_CURRENTREGION = SLR_AIS_SID_DT_AMUNDSEN
                    SLR_AIS_SID_TEMPSCALING_CURRENTREGION = SLR_AIS_SID_TEMPSCALING_AMUNDSEN
                    SLR_AIS_SID_R = SLR_AIS_SID_R_AMUNDSEN(1:NYEARS)
                ELSEIF (R == 2) THEN
                    SLR_AIS_SID_DT_CURRENTREGION = SLR_AIS_SID_DT_EASTANTARCTICA
                    SLR_AIS_SID_TEMPSCALING_CURRENTREGION = SLR_AIS_SID_TEMPSCALING_EASTANTARCTICA
                    SLR_AIS_SID_R = SLR_AIS_SID_R_EASTANTARCTICA(1:NYEARS)
                ELSEIF(R == 3) THEN
                    SLR_AIS_SID_DT_CURRENTREGION = SLR_AIS_SID_DT_ROSS
                    SLR_AIS_SID_TEMPSCALING_CURRENTREGION = SLR_AIS_SID_TEMPSCALING_ROSS
                    SLR_AIS_SID_R = SLR_AIS_SID_R_ROSS(1:NYEARS)
                ELSE
                    SLR_AIS_SID_DT_CURRENTREGION = SLR_AIS_SID_DT_WEDDELL
                    SLR_AIS_SID_TEMPSCALING_CURRENTREGION = SLR_AIS_SID_TEMPSCALING_WEDDELL
                    SLR_AIS_SID_R = SLR_AIS_SID_R_WEDDELL(1:NYEARS)
                END IF
                
                ! ACCOUNT FOR MELT DT            
                IF (AIS_SID_IDX >= SLR_AIS_SID_DT_CURRENTREGION) THEN
                    
                    ! UPDATE INDICES/COUNTERS IN LINE WITH SLR_AIS_SID_DT_CURRENTREGION
                    IF (SLR_AIS_SID_DT_CURRENTREGION == 0) THEN
                        AIS_SID_DT_STARTIDX = SLR_AIS_SID_STARTYEAR-STARTYEAR+1
                        AIS_SID_DT_IDX = AIS_SID_IDX
                    ELSE
                        AIS_SID_DT_STARTIDX = SLR_AIS_SID_STARTYEAR-STARTYEAR+1+ &
                            SLR_AIS_SID_DT_CURRENTREGION
                        AIS_SID_DT_IDX = AIS_SID_IDX - SLR_AIS_SID_DT_CURRENTREGION
                    END IF
                    
                    ! CALCULATE MELT FORCING
                    SLR_AIS_SID_OCNFORCE(R,CURRENT_YEAR_IDX) = &
                        SLR_AIS_SID_TEMPSCALING_CURRENTREGION * &
                        (DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(CURRENT_YEAR_IDX) - &
                        DAT_SURFACE_ANNUALMEANTEMP%DATGLOBE(AIS_SID_DT_STARTIDX)) * &                    
                        SLR_AIS_SID_BASALMELT_RANDOM
                    
                    SLR_AIS_SID_FORCING(R,CURRENT_YEAR_IDX) = &
                        SLR_AIS_SID_OCNFORCE(R,CURRENT_YEAR_IDX) - &
                        SLR_AIS_SID_OCNFORCE(R,AIS_SID_DT_STARTIDX)
                    
                    ! LAUNCH PIECE WISE CONVOLUTION
                    SLR_AIS_SID_CONV_CORNER_F(R,CURRENT_YEAR_IDX) = &
                        SLR_AIS_SID_FORCING(R,CURRENT_YEAR_IDX) * &
                        SLR_AIS_SID_R(1)
                    
                    IF (AIS_SID_DT_IDX > 1) THEN
                        SLR_AIS_SID_CONV_CORNER_R(R,CURRENT_YEAR_IDX) = &
                            SLR_AIS_SID_FORCING(R,AIS_SID_DT_STARTIDX) * &
                            SLR_AIS_SID_R(AIS_SID_DT_IDX)
                    END IF      
                    
                    IF (AIS_SID_DT_IDX > 2) THEN
                        DO I = 1, AIS_SID_DT_IDX-2
                            SLR_AIS_SID_CONV_MIDDLE(R,I) = &
                                SLR_AIS_SID_FORCING(R,CURRENT_YEAR_IDX-I) * &
                                SLR_AIS_SID_R(1+I)
                        END DO            
                        SLR_AIS_SID_CONV_MIDDLE_CUM(R,CURRENT_YEAR_IDX) = &
                            SUM(SLR_AIS_SID_CONV_MIDDLE(R,:))
                    END IF    
                    
                    ! COMBINE CONVOLUTION COMPONENTS FOR EACH TIME STEP
                    SLR_AIS_SID_CONV_STEPTOTAL(R,CURRENT_YEAR_IDX) = &
                        SLR_AIS_SID_CONV_CORNER_F(R,CURRENT_YEAR_IDX) + &
                    SLR_AIS_SID_CONV_MIDDLE_CUM(R,CURRENT_YEAR_IDX) + &
                        SLR_AIS_SID_CONV_CORNER_R(R,CURRENT_YEAR_IDX)
                    
                    ! CONVERT TOTAL CONVOLUTION SLE FROM M (LEVERMANN 2013) TO MM
                    SLR_AIS_SID_CONV_TOTAL(R,NEXT_YEAR_IDX) = &
                        SLR_AIS_SID_CONV_STEPTOTAL(R,CURRENT_YEAR_IDX) * 1000.0D0
                    
                END IF
            END DO
            
            ! SUM UP ALL REGIONAL CONVOLUTION RESULTS PROVIDING SLE IN MMPYEAR
            SLR_AIS_SID_CONTRIBUTION(NEXT_YEAR_IDX)= SUM(SLR_AIS_SID_CONV_TOTAL(:,NEXT_YEAR_IDX))
            
        END IF        
    END IF